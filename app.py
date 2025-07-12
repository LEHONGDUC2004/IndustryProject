import os
import shutil
import zipfile
import uuid
import subprocess
import time  # <-- Thêm thư viện time
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

# --- (1) THÔNG TIN CẤU HÌNH CẦN THAY ĐỔI ---
# Điền SSH URL của kho chứa Git trên GitHub/GitLab mà bạn muốn đẩy code lên.
# Ví dụ: 'git@github.com:your-username/my-deployment-repo.git'
GIT_REPO_SSH_URL = 'git@github.com:LEHONGDUC2004/IndustryProject.git'

# Thư mục tạm để xử lý các file upload
PROJECTS_BASE_DIR = 'temp_projects'
ALLOWED_EXTENSIONS = {'zip'}

# --- (2) CÀI ĐẶT FLASK ---
app = Flask(__name__)
app.secret_key = 'a-very-strong-secret-key-for-git-uploader'
# Tạo thư mục tạm nếu chưa có
os.makedirs(PROJECTS_BASE_DIR, exist_ok=True)


def allowed_file(filename):
    """Kiểm tra file có phải là .zip không"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_command(command, working_dir):
    """Hàm trợ giúp để chạy các lệnh command-line và xử lý lỗi"""
    print(f"Running command: {' '.join(command)} in {working_dir}")
    try:
        # Chạy lệnh và chờ nó hoàn thành
        result = subprocess.run(
            command,
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=True  # Tự động ném lỗi nếu lệnh thất bại (exit code != 0)
        )
        print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        # Ghi lại lỗi chi tiết từ stderr nếu lệnh thất bại
        print(f"Error running command: {' '.join(command)}")
        print(f"Stderr: {e.stderr}")
        return False, e.stderr


def process_and_push_to_git(file_object):
    """
    Hàm chính: nhận file, giải nén, và đẩy lên Git trên một nhánh mới.
    """
    # Tạo một ID duy nhất cho mỗi lần upload để tránh xung đột
    project_id = str(uuid.uuid4())
    project_path = os.path.join(PROJECTS_BASE_DIR, project_id)

    try:
        # --- BƯỚC A: CHUẨN BỊ THƯ MỤC CODE ---
        print(f"Creating temporary directory: {project_path}")
        os.makedirs(project_path)

        # Lưu và giải nén file zip
        safe_filename = secure_filename(file_object.filename)
        zip_path = os.path.join(project_path, safe_filename)
        file_object.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(project_path)
        os.remove(zip_path)  # Xóa file zip sau khi giải nén

        # --- BƯỚC B: THỰC THI CÁC LỆNH GIT ---
        # Tạo tên nhánh duy nhất, ví dụ: upload/my-website-a1b2c3d4
        branch_name = f"upload/{os.path.splitext(safe_filename)[0]}-{project_id[:8]}"

        # 1. Khởi tạo kho chứa Git
        success, _ = run_command(['git', 'init'], working_dir=project_path)
        if not success: raise Exception("Failed to initialize Git repository.")

        # Cấu hình user tạm thời cho commit này (không ảnh hưởng global)
        run_command(['git', 'config', 'user.name', '"Automated Deployer"'], working_dir=project_path)
        run_command(['git', 'config', 'user.email', '"bot@example.com"'], working_dir=project_path)

        # 2. Add và Commit code
        success, _ = run_command(['git', 'add', '.'], working_dir=project_path)
        if not success: raise Exception("Failed to add files to Git.")

        commit_message = f"Automated upload for project: {safe_filename}"
        success, _ = run_command(['git', 'commit', '-m', commit_message], working_dir=project_path)
        if not success: raise Exception("Failed to commit files.")

        # 3. Đổi tên nhánh, thêm remote và đẩy code
        success, _ = run_command(['git', 'branch', '-M', branch_name], working_dir=project_path)
        if not success: raise Exception("Failed to rename branch.")

        success, _ = run_command(['git', 'remote', 'add', 'origin', GIT_REPO_SSH_URL], working_dir=project_path)
        if not success: raise Exception("Failed to add remote Git origin.")

        # Đẩy nhánh mới lên server Git
        success, msg = run_command(['git', 'push', '-u', 'origin', branch_name], working_dir=project_path)
        if not success: raise Exception(f"Failed to push to Git: {msg}")

        # Nếu mọi thứ thành công, trả về tên nhánh để hiển thị cho người dùng
        return True, branch_name

    except Exception as e:
        # Bắt tất cả các lỗi khác và trả về thông báo
        print(f"An unexpected error occurred: {e}")
        return False, str(e)
    finally:
        # --- BƯỚC C: DỌN DẸP (ĐÃ SỬA LỖI CHO WINDOWS) ---
        # Luôn luôn xóa thư mục tạm sau khi hoàn tất, dù thành công hay thất bại
        if os.path.exists(project_path):
            print(f"Cleaning up temporary directory: {project_path}")
            try:
                shutil.rmtree(project_path)
            except PermissionError:
                # Nếu gặp lỗi PermissionError trên Windows, đợi một chút rồi thử lại
                print("PermissionError caught. Retrying after a short delay...")
                time.sleep(0.5)  # Đợi 0.5 giây
                shutil.rmtree(project_path, ignore_errors=True)


@app.route('/')
def index():
    """Hiển thị trang upload."""
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():  # <-- ĐÃ ĐỔI TÊN HÀM Ở ĐÂY
    """Xử lý request upload từ người dùng."""
    if 'file' not in request.files:
        flash('No file part in the request.')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected.')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Gọi hàm xử lý chính
        success, message = process_and_push_to_git(file)

        if success:
            flash(f"✅ Success! Project pushed to Git. Jenkins will start building shortly. Branch: {message}")
        else:
            flash(f"❌ Error! Failed to process project. Details: {message}")

        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a .zip file.')
        return redirect(request.url)


if __name__ == '__main__':
    # Chạy Flask app, cho phép truy cập từ các máy khác trong cùng mạng
    app.run(debug=True, host='0.0.0.0', port=5000)
