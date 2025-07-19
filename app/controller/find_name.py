import os

def find_executable_python_file(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            full_path = os.path.join(directory, filename)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "__name__" in content and "if __name__ == '__main__':" in content:
                        return filename
            except Exception as e:
                print(f"Lỗi khi đọc file {filename}: {e}")
                continue
    return None
