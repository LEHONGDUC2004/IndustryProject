import os
from app.controller.find_name import find_executable_python_file

def create_dockerfile(project_path, project_type):
    name_path = find_executable_python_file(project_path)

    if project_type not in ['static', 'nodejs', 'flask']:
        raise ValueError("Không nhận diện được loại ứng dụng. Vui lòng đảm bảo project hợp lệ.")

    dockerfile_path = os.path.join(project_path, 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        if project_type == 'static':
            f.write("""\
FROM nginx:stable-alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""")
        elif project_type == 'nodejs':
            f.write("""\
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
""")
        elif project_type == 'flask':
            f.write(f"""\
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["sh", "-c", "sleep 15 && python {name_path}"]
""")
