import os


def detect_project_type(project_path):
    if os.path.exists(os.path.join(project_path, 'package.json')):
        return 'nodejs'
    elif os.path.exists(os.path.join(project_path, 'app.py')) or os.path.exists(os.path.join(project_path, 'wsgi.py')) or os.path.exists(os.path.join(project_path, 'run.py')):
        return 'flask'
    else:
        return 'unknown'
