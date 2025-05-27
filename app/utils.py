import os
import uuid
from io import BytesIO
from google.cloud import storage, vision
from werkzeug.utils import secure_filename

def upload_image_to_gcs(file_stream, filename, bucket_name):
    """
    Upload an image to Google Cloud Storage
    
    Args:
        file_stream: File-like object containing image data
        filename: Original filename of the image
        bucket_name: Name of the GCS bucket to upload to
        
    Returns:
        Public URL of the uploaded file
    """
    # Create a unique filename to avoid collisions
    filename = secure_filename(filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    # Initialize GCS client with timeout settings
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"uploads/{unique_filename}")
        
        # Upload the file with timeout
        file_stream.seek(0)
        blob.upload_from_file(file_stream, timeout=30)
        
        # Make the blob publicly accessible with timeout
        blob.make_public(timeout=30)
        
        return blob.public_url
    except Exception as e:
        # Log and re-raise the exception to be handled by the caller
        import logging
        logging.error(f"GCS upload error: {str(e)}")
        raise

def analyze_image(file_stream):
    """
    Analyze an image using Google Cloud Vision API
    
    Args:
        file_stream: File-like object containing image data
        
    Returns:
        List of labels detected in the image
    """
    try:
        # Initialize Vision client
        vision_client = vision.ImageAnnotatorClient()
        
        # Read image content
        file_stream.seek(0)
        content = file_stream.read()
        
        # Create image object
        image = vision.Image(content=content)
        
        # Detect labels with timeout
        response = vision_client.label_detection(image=image, timeout=30)
        labels = response.label_annotations
        
        # Return list of labels
        return [label.description for label in labels]
    except Exception as e:
        # Log and re-raise the exception to be handled by the caller
        import logging
        logging.error(f"Vision API error: {str(e)}")
        # Return empty list instead of raising to allow application to continue
        return []