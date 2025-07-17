from flask import Blueprint, request, redirect, render_template
from werkzeug.utils import secure_filename
import os, zipfile, shutil, requests, logging

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)

# === Các thư mục mount volume từ Docker ===
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploaded")
EXTRACT_DIR = os.environ.get("EXTRACT_DIR", "/data/extracted")
REPLACED_DIR = os.environ.get("REPLACED_DIR", "/data/replaced")


JENKINS_URL = 'http://192.168.202.1:8081/job/build-web-static/buildWithParameters'
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '110eaba63ed58b2bf4c17121b75c764984'

for p in [UPLOAD_DIR, EXTRACT_DIR, REPLACED_DIR]:
    os.makedirs(p, exist_ok=True)

# === Kiểm tra định dạng file ===
ALLOWED_EXTENSIONS = {'zip'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# === Route hiển thị form upload ===
@upload_bp.route('/')
def index():
    return render_template('/upload')


# === Route xử lý upload ZIP ===
@upload_bp.route('/', methods=['POST'])
def upload_zip():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return 'Invalid file', 400

    filename = secure_filename(file.filename)
    zip_path = os.path.join(UPLOAD_DIR, filename)
    file.save(zip_path)

    # === Giải nén ===
    project_name = filename.rsplit('.', 1)[0]
    project_extract_path = os.path.join(EXTRACT_DIR, project_name)
    os.makedirs(project_extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(project_extract_path)

    # === Thêm Dockerfile vào thư mục đã giải nén ===
    dockerfile_path = os.path.join(project_extract_path, 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write("""\
FROM nginx:stable-alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""")

    # === Nén lại và đưa vào thư mục replaced ===
    replaced_zip_path = os.path.join(REPLACED_DIR, filename)
    shutil.make_archive(replaced_zip_path.rsplit('.', 1)[0], 'zip', project_extract_path)

    logger.info(f"✅ Đã xử lý ZIP: {filename}")
    trigger_jenkins_build(filename)

    return redirect('/')


def trigger_jenkins_build(zip_filename):
    payload = {
        'ZIP_NAME': zip_filename  # Truyền tên file, không phải path
    }
    response = requests.post(
        JENKINS_URL,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        params=payload
    )
    logger.info(f" Jenkins Triggered with ZIP_NAME={zip_filename}, status={response.status_code}")
    return response.status_code
