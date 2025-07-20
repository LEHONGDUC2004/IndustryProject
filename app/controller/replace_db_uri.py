import os

def replace_or_add_sqlalchemy_uri(file_path, db_info=None):
    if not os.path.exists(file_path):
        print(f"❌ Không tìm thấy file tại đường dẫn: {file_path}")
        return

    # Tạo dòng cấu hình mới
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
        inside_old_block = False
        replaced = False

        for line in lines:
            # Nếu đang ở block URI cũ thì bỏ qua tất cả dòng liên quan
            if "app.config['SQLALCHEMY_DATABASE_URI']" in line:
                inside_old_block = True
                replaced = True
                continue


            new_lines.append(line)

        # Chèn dòng mới vào trước return app
        inserted = False
        for i, line in enumerate(new_lines):
            if line.strip().startswith("return app"):
                if i > 0 and new_lines[i - 1].strip() != "":
                    new_lines.insert(i, "\n")
                    i += 1
                new_lines.insert(i, new_uri_line)
                inserted = True
                break

        if not inserted:
            new_lines.append("\n" + new_uri_line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"✅ Đã cập nhật SQLALCHEMY_DATABASE_URI trong file: {file_path}")

    except Exception as e:
        print(f"❌ Lỗi khi xử lý file {file_path}: {e}")
