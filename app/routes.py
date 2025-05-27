from flask import Blueprint, request, jsonify, current_app
from .models import db, Todo
from .utils import upload_image_to_gcs, analyze_image, cloud_executor
from werkzeug.exceptions import BadRequest
from io import BytesIO
import concurrent.futures

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    todo = Todo.query.get_or_404(todo_id)
    return jsonify(todo.to_dict())

@api.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo item"""
    if not request.is_json and 'title' not in request.form:
        return jsonify({"error": "Missing title"}), 400
    
    # Get data from JSON or form
    if request.is_json:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
    else:
        title = request.form.get('title')
        description = request.form.get('description', '')
    
    # Create new Todo instance
    todo = Todo(
        title=title,
        description=description
    )
    
    # Handle image upload if present
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename:
            # Create in-memory file
            image_stream = BytesIO()
            image_file.save(image_stream)
            
            # Upload to GCS with improved error handling
            bucket_name = current_app.config['GCS_BUCKET_NAME']
            try:
                # Use ThreadPoolExecutor with a timeout to prevent blocking
                future = cloud_executor.submit(upload_image_to_gcs, image_stream, image_file.filename, bucket_name)
                image_url = future.result(timeout=10)  # Wait up to 10 seconds for result
                todo.image_url = image_url
                
                # Process with ML API in background
                def process_image():
                    try:
                        image_stream.seek(0)
                        labels = analyze_image(image_stream)
                        if labels:
                            with current_app.app_context():
                                todo = Todo.query.get(todo.id)
                                if todo:
                                    todo.labels = ','.join(labels)
                                    db.session.commit()
                    except Exception as e:
                        current_app.logger.error(f"Background image analysis error: {str(e)}")
                
                # Submit the ML processing to run in background
                cloud_executor.submit(process_image)
            except concurrent.futures.TimeoutError:
                current_app.logger.error("GCS upload timed out - continuing without image")
            except Exception as e:
                current_app.logger.error(f"Error uploading image to GCS: {str(e)}")
                # Continue without image URL
    
    # Save to database
    db.session.add(todo)
    db.session.commit()
    
    return jsonify(todo.to_dict()), 201

@api.route('/todos/<int:todo_id>', methods=['PUT', 'PATCH'])
def update_todo(todo_id):
    """Update a todo item"""
    todo = Todo.query.get_or_404(todo_id)
    
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    
    # Update fields if provided
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed'] in [True, 'true', 'True', 1, '1']
    
    # Handle image upload if present
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename:
            # Create in-memory file
            image_stream = BytesIO()
            image_file.save(image_stream)
            
            # Upload to GCS with improved error handling
            bucket_name = current_app.config['GCS_BUCKET_NAME']
            try:
                # Use ThreadPoolExecutor with a timeout to prevent blocking
                future = cloud_executor.submit(upload_image_to_gcs, image_stream, image_file.filename, bucket_name)
                image_url = future.result(timeout=10)  # Wait up to 10 seconds for result
                todo.image_url = image_url
                
                # Process with ML API in background
                def process_image():
                    try:
                        image_stream.seek(0)
                        labels = analyze_image(image_stream)
                        if labels:
                            with current_app.app_context():
                                todo = Todo.query.get(todo.id)
                                if todo:
                                    todo.labels = ','.join(labels)
                                    db.session.commit()
                    except Exception as e:
                        current_app.logger.error(f"Background image analysis error: {str(e)}")
                
                # Submit the ML processing to run in background
                cloud_executor.submit(process_image)
            except concurrent.futures.TimeoutError:
                current_app.logger.error("GCS upload timed out - continuing without image")
            except Exception as e:
                current_app.logger.error(f"Error uploading image to GCS: {str(e)}")
                # Continue without updating image URL
    
    # Save changes
    db.session.commit()
    
    return jsonify(todo.to_dict())

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo item"""
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

@api.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": str(e)}), 400