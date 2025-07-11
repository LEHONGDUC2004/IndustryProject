# ✅ Flask App - Backend (VM1)
# Cho phép người dùng upload file .zip chứa website tĩnh
# Giải nén và gọi Jenkins job để build & run container trên VM2

import os
import zipfile
from flask import Flask, request, render_template, redirect
import requests
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
EXTRACT_FOLDER = 'extracted'
ALLOWED_EXTENSIONS = {'zip'}

# Jenkins server được cài trên máy thật Windows (IP 192.168.202.1)
JENKINS_URL = 'http://192.168.202.1/:8081/job/build-web-static/buildWithParameters'
JENKINS_USER = 'lehongduc3491'  # thay bằng user Jenkins thực tế
JENKINS_API_TOKEN = '110eaba63ed58b2bf4c17121b75c764984'  # thay bằng token từ Jenkins

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return 'Invalid file', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    extract_path = os.path.join(EXTRACT_FOLDER, filename[:-4])
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Gửi request đến Jenkins để build
    trigger_jenkins_build(extract_path)

    return redirect('/')

def trigger_jenkins_build(source_path):
    payload = {
        'SOURCE_PATH': source_path
    }
    response = requests.post(
        JENKINS_URL,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        params=payload
    )
    return response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
