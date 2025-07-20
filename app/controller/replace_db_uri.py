import os

def replace_or_add_sqlalchemy_uri(file_path, db_info=None):
    if not os.path.exists(file_path):
        print("Không tìm thấy file:", file_path)
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    replaced = False
    inside_old_block = False

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

    # Lọc bỏ dòng cũ
    for line in lines:
        if "app.config['SQLALCHEMY_DATABASE_URI']" in line:
            inside_old_block = True
            replaced = True
            continue
        if inside_old_block:
            if ')' in line or line.strip().endswith("'") or line.strip().endswith('"'):
                inside_old_block = False
            continue
        new_lines.append(line)

    # Chèn dòng mới nếu chưa có
    if not replaced:
        for i in range(len(new_lines)):
            if new_lines[i].strip().startswith("return app"):
                new_lines.insert(i, '\n' + new_uri_line)
                replaced = True
                break
        if not replaced:
            new_lines.append('\n' + new_uri_line)

    # Ghi lại file
    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    print("✅ Đã cập nhật SQLALCHEMY_DATABASE_URI trong", file_path)
