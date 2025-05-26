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
    
    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"uploads/{unique_filename}")
    
    # Upload the file
    file_stream.seek(0)
    blob.upload_from_file(file_stream)
    
    # Make the blob publicly accessible
    blob.make_public()
    
    return blob.public_url

def analyze_image(file_stream):
    """
    Analyze an image using Google Cloud Vision API
    
    Args:
        file_stream: File-like object containing image data
        
    Returns:
        List of labels detected in the image
    """
    # Initialize Vision client
    vision_client = vision.ImageAnnotatorClient()
    
    # Read image content
    file_stream.seek(0)
    content = file_stream.read()
    
    # Create image object
    image = vision.Image(content=content)
    
    # Detect labels
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations
    
    # Return list of labels
    return [label.description for label in labels]