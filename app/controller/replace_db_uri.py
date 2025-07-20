import os


def add_sqlalchemy_uri_if_missing(file_path, db_info=None):
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file tại đường dẫn: {file_path}")
        return

    # Step 1: Define the new URI line based on the provided db_info
    if db_info:
        new_uri_line = (
            f"    app.config['SQLALCHEMY_DATABASE_URI'] = "
            f"'mysql+pymysql://{db_info['DB_USER']}:{db_info['DB_PASSWORD']}@{db_info['DB_HOST']}/{db_info['DB_NAME']}?charset=utf8mb4'\n"
        )
    else:
        # Using a multi-line f-string for readability
        new_uri_line = (
            "    app.config['SQLALCHEMY_DATABASE_URI'] = (\n"
            "        f\"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4\"\n"
            "    )\n"
        )

    try:
        # Step 2: Read all lines and check if the config already exists
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        uri_exists = any("app.config['SQLALCHEMY_DATABASE_URI']" in line for line in lines)

        if uri_exists:
            print(f"Cấu hình SQLALCHEMY_DATABASE_URI đã tồn tại trong file: {file_path}. Không cần thêm.")
            return

        # Step 3: If it doesn't exist, find the insertion point and add the line
        new_lines = []
        inserted = False
        for line in lines:
            # Insert the new URI just before 'return app'
            if line.strip().startswith("return app") and not inserted:
                # Add a blank line for spacing if the previous line wasn't empty
                if new_lines and new_lines[-1].strip() != "":
                    new_lines.append('\n')
                new_lines.append(new_uri_line)
                inserted = True

            new_lines.append(line)

        # Fallback if 'return app' is not found
        if not inserted:
            if new_lines and new_lines[-1].strip() != "":
                new_lines.append('\n')
            new_lines.append(new_uri_line)

        # Step 4: Write the new content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"✅ Đã thêm thành công SQLALCHEMY_DATABASE_URI vào file: {file_path}")

    except IOError as e:
        print(f"Lỗi khi đọc/ghi file: {e}")
    except Exception as e:
        print(f"Đã có lỗi không mong muốn xảy ra: {e}")