import os

def replace_or_add_sqlalchemy_uri(file_path, db_info=None):
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file tại đường dẫn: {file_path}")
        return

    # Tạo dòng URI mới
    if db_info:
        new_uri_line = (
            f"app.config['SQLALCHEMY_DATABASE_URI'] = "
            f"'mysql+pymysql://{db_info['DB_USER']}:{db_info['DB_PASSWORD']}@{db_info['DB_HOST']}/{db_info['DB_NAME']}?charset=utf8mb4'\n"
        )
    else:
        new_uri_line = (
            "app.config['SQLALCHEMY_DATABASE_URI'] = (\n"
            "    f\"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4\"\n"
            ")\n"
        )

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        inserted = False
        replaced = False
        insert_index = None
        base_indent = ""

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Nếu là dòng chứa app = Flask(__name__)
            if 'app = Flask(__name__)' in stripped:
                insert_index = i + 1
                base_indent = line[:len(line) - len(line.lstrip())]

            # Nếu là dòng chứa URI cũ (dù có thụt dòng hay không)
            if (
                "app.config[" in stripped and
                "SQLALCHEMY_DATABASE_URI" in stripped and
                (
                    "'mysql+pymysql://" in stripped or
                    '"mysql+pymysql://' in stripped or
                    '%quote(' in stripped
                )
            ):
                replaced = True
                continue  # Xoá dòng này

            new_lines.append(line)

        # Chèn dòng mới sau Flask khởi tạo
        if insert_index is not None:
            new_lines.insert(insert_index, base_indent + new_uri_line)
            inserted = True

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        # Thông báo
        if replaced and inserted:
            print(f"Đã thay thế URI cũ bằng URI mới trong: {file_path}")
        elif inserted:
            print(f"Đã thêm URI mới vào sau Flask khởi tạo trong: {file_path}")
        else:
            print(f"Không tìm thấy Flask app để chèn URI mới trong: {file_path}")

    except Exception as e:
        print(f"Lỗi khi xử lý file {file_path}: {e}")
