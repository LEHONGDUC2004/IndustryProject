import os

def replace_or_add_sqlalchemy_uri(file_path, db_info=None):
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file tại đường dẫn: {file_path}")
        return

    # Tạo dòng URI mới
    if db_info:
        new_uri_line = (
            f"    app.config['SQLALCHEMY_DATABASE_URI'] = "
            f"'mysql+pymysql://{db_info['DB_USER']}:{db_info['DB_PASSWORD']}@{db_info['DB_HOST']}/{db_info['DB_NAME']}?charset=utf8mb4'\n"
        )
    else:
        new_uri_line = (
            "    app.config['SQLALCHEMY_DATABASE_URI'] = (\n"
            "        f\"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4\"\n"
            "    )\n"
        )

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        replaced = False
        inserted = False

        for i, line in enumerate(lines):
            # Bỏ dòng URI cũ nếu có
            if "app.config['SQLALCHEMY_DATABASE_URI']" in line:
                replaced = True
                continue

            new_lines.append(line)

            # Tìm vị trí ngay sau dòng Flask app = ...
            if not inserted and 'app = Flask(__name__)' in line:
                new_lines.append(new_uri_line)
                inserted = True

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        if replaced:
            print(f"Đã thay thế SQLALCHEMY_DATABASE_URI trong file: {file_path}")
        elif inserted:
            print(f"Đã thêm SQLALCHEMY_DATABASE_URI vào file: {file_path}")
        else:
            print(f"Không tìm thấy vị trí phù hợp để chèn URI trong: {file_path}")

    except Exception as e:
        print(f"Lỗi khi xử lý file {file_path}: {e}")
