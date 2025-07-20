import os
def replace_sqlalchemy_uri(file_path, db_info=None):
    if not os.path.exists(file_path):
        print("Không tìm thấy file:", file_path)
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    replaced = False

    # Nếu truyền db_info thì render URI cụ thể
    if db_info:
        new_uri = (
            f"mysql+pymysql://{db_info['DB_USER']}:{db_info['DB_PASSWORD']}@{db_info['DB_HOST']}/{db_info['DB_NAME']}?charset=utf8mb4"
        )
        uri_line = f"    app.config['SQLALCHEMY_DATABASE_URI'] = '{new_uri}'\n"
    else:
        # Mặc định dùng os.getenv
        uri_line = (
            "    app.config['SQLALCHEMY_DATABASE_URI'] = (\n"
            "        f\"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4\"\n"
            "    )\n"
        )

    for line in lines:
        if "app.config['SQLALCHEMY_DATABASE_URI']" in line:
            if not replaced:
                new_lines.append(uri_line)
                replaced = True
            continue
        new_lines.append(line)

    if not replaced:
        new_lines.append("\n" + uri_line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    print(" Đã thay đổi SQLALCHEMY_DATABASE_URI trong", file_path)
