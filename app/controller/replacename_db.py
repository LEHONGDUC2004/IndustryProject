import re

def replace_database_name(sql_path, new_db_name):
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Tìm tên cũ trong câu lệnh CREATE DATABASE hoặc USE
    match = re.search(r'(CREATE DATABASE|USE)\s+`?([a-zA-Z0-9_]+)`?', sql_content, re.IGNORECASE)
    if match:
        old_name = match.group(2)
        print(f"Phát hiện database cũ: {old_name} → sẽ thay bằng: {new_db_name}")

        # Thay toàn bộ tên cũ bằng tên mới
        sql_content = re.sub(rf'\b{old_name}\b', new_db_name, sql_content)

        with open(sql_path, 'w', encoding='utf-8') as f:
            f.write(sql_content)
    else:
        print("Không tìm thấy tên database cũ trong file .sql")
