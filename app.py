import os
import zipfile
import shutil
import requests
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Đọc biến môi trường để xác định các thư mục
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploaded")
EXTRACT_DIR = os.environ.get("EXTRACT_DIR", "/data/extracted")
REPLACED_DIR = os.environ.get("REPLACED_DIR", "/data/replaced")

JENKINS_URL = 'http://192.168.202.1:8081/job/build-web-static/buildWithParameters'
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '110eaba63ed58b2bf4c17121b75c764984'

ALLOWED_EXTENSIONS = {'zip'}

# Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

# Tạo thư mục nếu chưa có
for path in [UPLOAD_DIR, EXTRACT_DIR, REPLACED_DIR]:
    os.makedirs(path, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_zip():
    if 'file' not in request.files:
        return '❌ No file part', 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return '❌ Invalid file', 400

    filename = secure_filename(file.filename)
    zip_path = os.path.join(UPLOAD_DIR, filename)
    file.save(zip_path)

    project_name = filename.rsplit('.', 1)[0]
    project_extract_path = os.path.join(EXTRACT_DIR, project_name)
    os.makedirs(project_extract_path, exist_ok=True)

    # ✅ Giải nén
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(project_extract_path)

    # ✅ Thêm Dockerfile
    dockerfile_path = os.path.join(project_extract_path, 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write("""\
FROM nginx:stable-alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""")

    # ✅ Nén lại vào replaced folder
    replaced_zip_path = os.path.join(REPLACED_DIR, filename)
    shutil.make_archive(replaced_zip_path.rsplit('.', 1)[0], 'zip', project_extract_path)

    logger.info(f"✅ Đã xử lý: {filename}")
    trigger_jenkins_build(replaced_zip_path)
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
