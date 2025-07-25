import os
import re
from app.controller.find_name import find_executable_python_file


def find_port_host(project_path):
    target_file_rel = find_executable_python_file(project_path)
    if not target_file_rel:
        return None

    target_file_path = os.path.join(project_path, target_file_rel)

    try:
        with open(target_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Tìm dòng app.run(...)
        pattern = r'app\.run\((.*?)\)'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return None

        args_str = match.group(1)

        # Kiểm tra nếu chưa có host thì thêm host='0.0.0.0'
        if "host=" not in args_str:
            args_str += ", host='0.0.0.0'"

        # Thay thế port hiện tại nếu có bằng 5000
        if "port=" in args_str:
            args_str = re.sub(r'port\s*=\s*\d+', 'port=5000', args_str)
        else:
            args_str += ", port=5000"

        # Xây dựng dòng mới
        new_run_line = f"app.run({args_str})"

        # Thay thế dòng cũ bằng dòng mới trong nội dung file
        new_content = re.sub(pattern, new_run_line, content, flags=re.DOTALL)

        # Ghi lại nội dung mới vào file
        with open(target_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return target_file_rel

    except Exception as e:
        print(f"[!] Không thể cập nhật file {target_file_path}: {e}")
        return None
