import os
import zipfile
from flask import Flask, request, render_template, redirect
import requests
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app_logger = logging.getLogger(__name__)

# Use environment variables (default to safe container paths)
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/uploads')
EXTRACT_FOLDER = os.environ.get('EXTRACT_FOLDER', '/app/extracted')
ALLOWED_EXTENSIONS = {'zip'}

# Jenkins info
JENKINS_URL = 'http://192.168.202.1:8081/job/build-web-static/buildWithParameters'
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '110eaba63ed58b2bf4c17121b75c764984'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload & extracted folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
app_logger.info(f"UPLOAD_FOLDER = {UPLOAD_FOLDER}")
app_logger.info(f"EXTRACT_FOLDER = {EXTRACT_FOLDER}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    app_logger.info("Upload request received")
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return 'Invalid file', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(filepath)
        app_logger.info(f"File saved: {filepath}")
    except Exception as e:
        return f"Save failed: {e}", 500

    project_name = filename[:-4] if filename.endswith('.zip') else filename
    extract_path = os.path.join(EXTRACT_FOLDER, project_name)
    os.makedirs(extract_path, exist_ok=True)

    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        app_logger.info(f"Extracted to: {extract_path}")
    except Exception as e:
        return f"Extract failed: {e}", 500

    trigger_jenkins_build(project_name)
    return redirect('/')

def trigger_jenkins_build(project_name):
    payload = {'PROJECT_NAME': project_name}
    try:
        res = requests.post(
            JENKINS_URL,
            auth=(JENKINS_USER, JENKINS_API_TOKEN),
            params=payload,
            timeout=30
        )
        app_logger.info(f"Triggered Jenkins with status: {res.status_code}")
    except Exception as e:
        app_logger.error(f"Jenkins trigger error: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
