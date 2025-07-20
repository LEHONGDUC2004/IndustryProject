from flask import Blueprint, request, redirect, session, logging, url_for
from werkzeug.utils import secure_filename
from app.controller.allowed_file import allowed_file
from app.controller.detect_project import detect_project_type
from app.controller.create_dockerfile import create_dockerfile
from app.controller.create_dockercompose import create_compose
from app.controller.convert_db import import_sql_to_mysql
from app.controller.replace_db_uri import replace_or_add_sqlalchemy_uri

import os, shutil, zipfile, subprocess

from app.routes.jenkins_trigger import trigger_jenkins_build

uploadAll_bp = Blueprint('upload_all', __name__)


UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploaded")
EXTRACT_DIR = os.environ.get("EXTRACT_DIR", "/data/extracted")
REPLACED_DIR = os.environ.get("REPLACED_DIR", "/data/replaced")

# Đảm bảo các thư mục tồn tại khi container chạy ===
for p in [UPLOAD_DIR, EXTRACT_DIR, REPLACED_DIR]:
    os.makedirs(p, exist_ok=True)

@uploadAll_bp.route('/upload_all', methods=['POST'])
def upload_all():

    # 1. Lấy thông tin DB
    db_info = {
        'DB_NAME': request.form.get('name_database'),
        'DB_USER': request.form.get('name_user'),
        'DB_HOST': request.form.get('host_db'),
        'DB_PASSWORD': request.form.get('passwd')
    }
    session['db_info'] = db_info

    # 2. Lưu file .sql
    sql_file = request.files.get('file_sql')
    sql_filename = secure_filename(sql_file.filename)
    sql_path = os.path.join(UPLOAD_DIR, sql_filename)
    sql_file.save(sql_path)

    # 3. Lưu và giải nén file .zip
    zip_file = request.files.get('file_zip')
    zip_filename = secure_filename(zip_file.filename)
    zip_path = os.path.join(UPLOAD_DIR, zip_filename)
    zip_file.save(zip_path)
    if zip_filename == '' or not allowed_file(zip_filename):
        return 'Invalid file', 400

    # Giải nén
    project_name = zip_filename.rsplit('.', 1)[0]
    extract_path = os.path.join(EXTRACT_DIR, project_name)
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Nếu có 1 thư mục duy nhất bên trong
    subdirs = [d for d in os.listdir(extract_path) if os.path.isdir(os.path.join(extract_path, d))]
    project_real_path = os.path.join(extract_path, subdirs[0]) if len(subdirs) == 1 else extract_path


    # Tìm file __init__.py để thay thế dòng URI cứng
    init_file_path = os.path.join(project_real_path, 'app', '__init__.py')
    replace_or_add_sqlalchemy_uri(init_file_path, db_info)

    # 5. Tạo Dockerfile + docker-compose
    project_type = detect_project_type(project_real_path)
    create_dockerfile(project_real_path, project_type)
    create_compose(
        docker_path=project_real_path,
        name_database=db_info['DB_NAME'],
        name_user=db_info['DB_USER'],
        host_db=db_info['DB_HOST'],
        passwd=db_info['DB_PASSWORD']
    )

    # 6. Tự động import file .sql
    import_sql_to_mysql(sql_path, db_info)

    # 7. Nén lại dự án đã xử lý
    replaced_path = os.path.join(REPLACED_DIR, zip_filename)
    shutil.make_archive(
        replaced_path.rsplit('.', 1)[0],
        'zip',
        root_dir=os.path.dirname(project_real_path),
        base_dir=os.path.basename(project_real_path)
    )

    trigger_jenkins_build(zip_filename)

    return redirect(url_for('main.success'))  # cách này chỉ đúng nếu dùng route thuần


