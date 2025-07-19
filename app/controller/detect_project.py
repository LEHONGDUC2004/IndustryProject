import os


def detect_project_type(project_path):
    for filename in os.listdir(project_path):
        if filename.endswith('.json'):
                return 'nodejs'
        elif filename.endswith('.py'):
                return 'flask'
        elif filename.endswith('.html'):
                return "static"
        else:
                return 'unknown'
