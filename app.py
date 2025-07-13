import os
import zipfile
from flask import Flask, request, render_template, redirect
import requests
from werkzeug.utils import secure_filename
import logging # Import logging module

# Configure logging for better visibility in container logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app_logger = logging.getLogger(__name__)

# Use environment variables for paths, defaulting to absolute paths inside the container
# These paths MUST match the target paths in your docker-compose.yml volumes section
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/data/uploads')
EXTRACT_FOLDER = os.environ.get('EXTRACT_FOLDER', '/data/extracted')
ALLOWED_EXTENSIONS = {'zip'}

# Jenkins connection details
JENKINS_URL = 'http://192.168.202.1:8081/job/build-web-static/buildWithParameters'
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '110eaba63ed58b2bf4c17121b75c764984'

app = Flask(__name__)
# Flask will use this for file.save, so it must point to the mounted volume
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the directories exist *inside the container* when the app starts.
# These will correspond to the mounted host directories.
# This is crucial for the app to be able to write files.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
app_logger.info(f"Initialized UPLOAD_FOLDER: {UPLOAD_FOLDER}")
app_logger.info(f"Initialized EXTRACT_FOLDER: {EXTRACT_FOLDER}")


def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Renders the upload form."""
    # Assuming upload.html exists in the 'templates' folder
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file upload, extraction, and triggers Jenkins build."""
    app_logger.info("Received upload request.")
    if 'file' not in request.files:
        app_logger.warning("No file part in the request.")
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        app_logger.warning(f"Invalid file uploaded: {file.filename}")
        return 'Invalid file', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
        app_logger.info(f"File '{filename}' saved to {filepath}")
    except Exception as e:
        app_logger.error(f"Error saving file '{filename}' to {filepath}: {e}")
        return f"Error saving file: {e}", 500

    project_name = filename[:-4] if filename.endswith('.zip') else filename # e.g., "my_project.zip" becomes "my_project"
    extract_path_in_container = os.path.join(EXTRACT_FOLDER, project_name)
    
    # Create the specific extraction directory inside the mounted volume
    os.makedirs(extract_path_in_container, exist_ok=True)
    app_logger.info(f"Created extraction directory: {extract_path_in_container}")

    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_path_in_container)
        app_logger.info(f"File '{filename}' extracted to {extract_path_in_container}")
    except zipfile.BadZipFile:
        app_logger.error(f"Failed to extract '{filename}': Not a valid zip file.")
        return 'Failed to extract zip file: Not a valid ZIP file.', 500
    except Exception as e:
        app_logger.error(f"An error occurred during extraction of '{filename}': {e}")
        return f"An error occurred during extraction: {e}", 500

    # Trigger Jenkins build, passing the project name.
    # Jenkins job will be responsible for locating this project on VM1's host filesystem.
    trigger_jenkins_build(project_name)
    
    # Optionally, delete the uploaded zip file after extraction to save space
    # os.remove(filepath) 
    # app_logger.info(f"Removed uploaded zip file: {filepath}")

    return redirect('/')

def trigger_jenkins_build(project_name):
    """Triggers a Jenkins build with the project name."""
    # The Jenkins job 'build-web-static' needs to be updated to accept 'PROJECT_NAME'
    # and then use scp to fetch /home/lehongduc3491/IndustryProject/extracted/{PROJECT_NAME} from VM1
    payload = {
        'PROJECT_NAME': project_name # Sending the project name, not a full path on VM1
    }
    app_logger.info(f"Attempting to trigger Jenkins build for project: '{project_name}' at {JENKINS_URL}")
    try:
        response = requests.post(
            JENKINS_URL,
            auth=(JENKINS_USER, JENKINS_API_TOKEN),
            params=payload,
            timeout=30 # Increased timeout for potentially slow Jenkins response
        )
        if response.status_code == 200 or response.status_code == 201: # 201 for 'Created'
            app_logger.info(f"Jenkins build triggered successfully for project: '{project_name}'. Status: {response.status_code}")
        else:
            app_logger.error(f"Failed to trigger Jenkins build. Status: {response.status_code}, Response: {response.text}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        app_logger.error(f"Error connecting to Jenkins: {e}")
        return 500 # Return an error status code

if __name__ == '__main__':
    # When running locally without Docker Compose, these paths would be relative to app.py
    # But in Docker Compose, they will be overridden by environment variables and mounts.
    app.run(debug=True, host='0.0.0.0')

