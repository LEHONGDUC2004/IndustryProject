import os

def find_entrypoint_and_pythonpath(project_root):
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'app = Flask(__name__)' in content and 'app.run' in content:
                            rel_path = os.path.relpath(full_path, project_root)
                            module_dir = os.path.dirname(rel_path)
                            pythonpath = os.path.normpath(os.path.join(project_root, module_dir))
                            print(f"✅ Đã tìm thấy file chạy chính: {rel_path}")
                            print(f"🔍 PYTHONPATH phù hợp là: {module_dir or '.'}")
                            return rel_path, module_dir or "."
                except Exception as e:
                    print(f"❌ Lỗi đọc file {full_path}: {e}")
    print("⚠️ Không tìm thấy file phù hợp.")
    return None, None
