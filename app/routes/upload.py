# app/backend/upload.py
from flask import Blueprint, render_template, request, redirect
import os, zipfile, shutil
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/')
def index():
    return render_template('upload.html')

@upload_bp.route('/upload', methods=['POST'])
def upload_zip():
        if 'file' not in request.files:
            return ' No file part', 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return ' Invalid file', 400

        filename = secure_filename(file.filename)
        zip_path = os.path.join(UPLOAD_DIR, filename)
        file.save(zip_path)

        # Giải nén
        project_name = filename.rsplit('.', 1)[0]
        project_extract_path = os.path.join(EXTRACT_DIR, project_name)
        os.makedirs(project_extract_path, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(project_extract_path)

        # Thêm Dockerfile
        dockerfile_path = os.path.join(project_extract_path, 'Dockerfile')
        with open(dockerfile_path, 'w') as f:
            f.write("""\
    FROM nginx:stable-alpine
    COPY . /usr/share/nginx/html
    EXPOSE 80
    CMD ["nginx", "-g", "daemon off;"]
    """)

        # Nén lại vào thư mục replaced
        replaced_zip_path = os.path.join(REPLACED_DIR, filename)
        shutil.make_archive(replaced_zip_path.rsplit('.', 1)[0], 'zip', project_extract_path)

        logger.info(f" Đã xử lý: {filename}")
        trigger_jenkins_build(filename)

        return redirect('/')
