import os

def replace_or_add_sqlalchemy_uri(file_path, db_info=None):
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file tại đường dẫn: {file_path}")
        return

    # Tạo dòng mới
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

        for line in lines:
            # XÓA nếu là dòng URI hardcoded hoặc dùng %quote()
            if (
                "app.config[" in line and
                "SQLALCHEMY_DATABASE_URI" in line and
                (
                    '"mysql+pymysql://' in line or
                    "'mysql+pymysql://" in line
                )
            ):
                replaced = True
                continue  # bỏ dòng này

            new_lines.append(line)

            # Chèn sau Flask khởi tạo
            if not inserted and "Flask(__name__)" in line:
                new_lines.append(new_uri_line)
                inserted = True

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        if replaced:
            print(f"Đã xóa dòng SQLALCHEMY_DATABASE_URI cũ và thêm dòng mới trong: {file_path}")
        elif inserted:
            print(f"Đã thêm URI mới (không thấy dòng cũ) vào: {file_path}")
        else:
            print(f"Không thấy Flask app để chèn dòng mới trong: {file_path}")

    except Exception as e:
        print(f"Lỗi xử lý {file_path}: {e}")
