from flask import Blueprint, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from app.controller.allowed_file import allowed_file
from app.controller.detect_project import detect_project_type
from app.controller.create_dockerfile import create_dockerfile
from app.controller.create_dockercompose import create_compose
from app.controller.convert_db import import_sql_to_mysql
from app.controller.replace_db_uri import replace_or_add_sqlalchemy_uri
from app.controller.replacename_db import replace_database_name
from app.controller.find_init_file import find_flask_app_file
from app.controller.test_requirements import ensure_requirements_at_root
from app.routes.jenkins_trigger import trigger_jenkins_build
from app.controller.test_host_port import find_port_host
from app.controller.count_file_zip import count_uploaded_zips


import os
import shutil
import zipfile

uploadAll_bp = Blueprint('upload_all', __name__)

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploaded")
EXTRACT_DIR = os.environ.get("EXTRACT_DIR", "/data/extracted")
REPLACED_DIR = os.environ.get("REPLACED_DIR", "/data/replaced")

# Ensure directories exist
for p in [UPLOAD_DIR, EXTRACT_DIR, REPLACED_DIR]:
    os.makedirs(p, exist_ok=True)

def get_next_index_from_folder(base_dir="/data/deploy"):
    existing = [name for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name))]
    return len(existing) + 1

@uploadAll_bp.route('/upload_all', methods=['POST'])
def upload_all():
    # 1. Get DB info
    db_info = {
        'DB_NAME': request.form.get('name_database'),
        'DB_USER': request.form.get('name_user'),
        'DB_HOST': request.form.get('host_db') or 'db',  # fallback if empty
        'DB_PASSWORD': request.form.get('passwd')
    }
    session['db_info'] = db_info

    # 2. Save .sql file if exists
    sql_file = request.files.get('file_sql')
    sql_filename = None
    if sql_file and sql_file.filename:
        sql_filename = secure_filename(sql_file.filename)
        sql_path = os.path.join(UPLOAD_DIR, sql_filename)
        sql_file.save(sql_path)

        replace_database_name(sql_path=sql_path,
                              new_db_name=db_info['DB_NAME'],
                              db_user=db_info['DB_USER'],
                              db_password=db_info['DB_PASSWORD'])

        import_sql_to_mysql(sql_path, db_info)

    # 3. Handle ZIP file
    zip_file = request.files.get('file_zip')
    if not zip_file or not allowed_file(zip_file.filename):
        return 'Invalid ZIP file.', 400

    zip_filename = secure_filename(zip_file.filename)
    zip_path = os.path.join(UPLOAD_DIR, zip_filename)
    zip_file.save(zip_path)
    # Count file zip
    zip_count = count_uploaded_zips(UPLOAD_DIR)
    # Extract project
    project_name = zip_filename.rsplit('.', 1)[0]
    extract_path = os.path.join(EXTRACT_DIR, project_name)
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    subdirs = [d for d in os.listdir(extract_path) if os.path.isdir(os.path.join(extract_path, d))]
    project_real_path = os.path.join(extract_path, subdirs[0]) if len(subdirs) == 1 else extract_path

    ensure_requirements_at_root(project_real_path)

    # Copy .sql file into project if exists
    if sql_filename:
        shutil.copy(sql_path, os.path.join(project_real_path, sql_filename))

    find_port_host(project_real_path)

    init_file_path = find_flask_app_file(project_real_path)
    replace_or_add_sqlalchemy_uri(init_file_path, db_info)

    project_type = detect_project_type(project_real_path)
    create_dockerfile(project_real_path, project_type)
    create_compose(docker_path=project_real_path,
                   name_database=db_info['DB_NAME'],
                   name_user=db_info['DB_USER'],
                   host_db=db_info['DB_HOST'],
                   passwd=db_info['DB_PASSWORD'],
                   filename_sql=sql_filename,
                   index=zip_count)

    # 7. Compress modified project
    replaced_path = os.path.join(REPLACED_DIR, zip_filename)
    shutil.make_archive(replaced_path.rsplit('.', 1)[0], 'zip',
                        root_dir=os.path.dirname(project_real_path),
                        base_dir=os.path.basename(project_real_path))

    trigger_jenkins_build(zip_filename)

    return redirect(url_for('main.success'))