# Flask TODO Application

A Flask-based Todo management application with image upload and automatic classification capabilities.

## Features

- RESTful API for Todo management (create, read, update, delete)
- Image upload functionality with Google Cloud Storage
- Automatic image classification using Google Cloud Vision API
- CI/CD pipeline with GitHub Actions
- Deployment to Google Cloud Run

## API Endpoints

- `GET /api/todos` - List all todos
- `GET /api/todos/{id}` - Get a specific todo
- `POST /api/todos` - Create a new todo
- `PUT/PATCH /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo

## Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/miyabi-org/flask-todo.git
   cd flask-todo
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   export DB_HOST=localhost
   export DB_USER=postgres
   export DB_PASSWORD=password
   export DB_PORT=5432
   export DB_NAME=todo
   export GCS_BUCKET_NAME=your-bucket-name
   ```

4. Run the application:
   ```
   python main.py
   ```

## Deployment

The application is automatically deployed to Google Cloud Run when changes are pushed to the main branch.