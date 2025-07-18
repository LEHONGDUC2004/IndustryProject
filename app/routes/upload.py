from flask import Blueprint, request, redirect, render_template
from app.routes.jenkins_trigger import trigger_jenkins_build
from werkzeug.utils import secure_filename
import os, zipfile, shutil, requests, logging
from app.controller.allowed_file import allowed_file
from app.controller.detect_project import detect_project_type
from app.controller.create_dockerfile import create_dockerfile
from app.controller.create_dockercompose import create_compose

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)

# === Các thư mục mount volume từ Docker ===
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploaded")
EXTRACT_DIR = os.environ.get("EXTRACT_DIR", "/data/extracted")
REPLACED_DIR = os.environ.get("REPLACED_DIR", "/data/replaced")

for p in [UPLOAD_DIR, EXTRACT_DIR, REPLACED_DIR]:
    os.makedirs(p, exist_ok=True)

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

    # === Tìm thư mục project thực sự bên trong nếu tồn tại ===
    items = os.listdir(project_extract_path)
    subdirs = [d for d in items if os.path.isdir(os.path.join(project_extract_path, d))]
    if len(subdirs) == 1:
        project_real_path = os.path.join(project_extract_path, subdirs[0])
    else:
        project_real_path = project_extract_path

    # === Phân loại dự án (Python, Node.js, v.v.) ===
    project_type = detect_project_type(project_real_path)

    # === Thêm Dockerfile & docker-compose.yml nếu chưa có ===
    dockerfile_path = os.path.join(project_real_path, "Dockerfile")
    compose_path = os.path.join(project_real_path, "docker-compose.yml")

    if not os.path.exists(dockerfile_path):
        create_dockerfile(project_real_path, project_type)

    if not os.path.exists(compose_path):
        create_compose(project_real_path)

    # === Nén lại dự án sau khi xử lý ===
    replaced_zip_path = os.path.join(REPLACED_DIR, filename)
    shutil.make_archive(
        replaced_zip_path.rsplit('.', 1)[0],
        'zip',
        root_dir=os.path.dirname(project_real_path),
        base_dir=os.path.basename(project_real_path)
    )

    logger.info(f"Đã xử lý ZIP: {filename}")
    trigger_jenkins_build(filename)

    return redirect('/')
