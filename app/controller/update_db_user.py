import os
from urllib.parse import quote

def update_database_uri_in_project(project_path, db_info):
    """
    Cập nhật hoặc thêm mới dòng SQLALCHEMY_DATABASE_URI trong file .env của project người dùng upload.
    Nếu đã có, sẽ xóa dòng cũ trước khi thêm dòng mới.
    """
    env_path = os.path.join(project_path, '.env')

    # Tạo URI mới
    new_uri = (
        f"mysql+pymysql://{db_info['DB_USER']}:{db_info['DB_PASSWORD']}"
        f"@{db_info['DB_HOST']}/{db_info['DB_NAME']}?charset=utf8mb4"
    )
    new_line = f"SQLALCHEMY_DATABASE_URI={new_uri}"

    # Nếu file .env chưa tồn tại, tạo mới và ghi luôn
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            f.write(f"{new_line}\n")
        return

    # Đọc toàn bộ nội dung
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Lọc bỏ dòng cũ nếu có
    filtered_lines = [line for line in lines if not line.strip().startswith("SQLALCHEMY_DATABASE_URI=")]

    # Thêm dòng mới vào cuối
    filtered_lines.append(f"{new_line}\n")

    # Ghi lại toàn bộ file
    with open(env_path, 'w') as f:
        f.writelines(filtered_lines)
