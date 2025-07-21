import os

def find_executable_python_file(project_path):
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '__main__' in content and 'app.run' in content:
                        # Trả về đường dẫn tính từ thư mục gốc Docker (/app)
                        return os.path.relpath(full_path, project_path)
    return None

