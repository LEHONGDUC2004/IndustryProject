import os

def replace_sqlalchemy_uri(file_path):
    if not os.path.exists(file_path):
        print("Không tìm thấy file:", file_path)
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Xoá dòng cũ nếu chứa SQLALCHEMY_DATABASE_URI
    new_lines = []
    replaced = False
    for line in lines:
        if "app.config['SQLALCHEMY_DATABASE_URI']" in line:
            if not replaced:
                # Thêm dòng mới (chỉ thêm 1 lần)
                new_lines.append("    app.config['SQLALCHEMY_DATABASE_URI'] = (\n")
                new_lines.append("        f\"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4\"\n")
                new_lines.append("    )\n")
                replaced = True
            # Bỏ qua dòng cũ
            continue
        new_lines.append(line)

    # Nếu chưa có dòng nào thì thêm mới
    if not replaced:
        new_lines.append("\n    app.config['SQLALCHEMY_DATABASE_URI'] = (\n")
        new_lines.append("        f\"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4\"\n")
        new_lines.append("    )\n")

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    print("✅ Đã thay đổi SQLALCHEMY_DATABASE_URI trong", file_path)
