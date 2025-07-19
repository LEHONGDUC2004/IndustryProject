import os

def detect_project_type(project_path):
    has_json = False
    has_py = False
    has_html = False

    for filename in os.listdir(project_path):
        if filename.endswith('.json'):
            has_json = True
        elif filename.endswith('.py'):
            has_py = True
        elif filename.endswith('.html'):
            has_html = True

    if has_json:
        return 'nodejs'
    elif has_py:
        return 'flask'
    elif has_html:
        return 'static'
    else:
        return 'unknown'
