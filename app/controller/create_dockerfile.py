import os
from app.controller.find_entrypoint_and_pythonpath import find_entrypoint_and_pythonpath # Trả về entrypoint và python_path

def create_dockerfile(project_path, project_type):
    project_name = os.path.basename(os.path.abspath(project_path))
    if project_type not in ['static', 'nodejs', 'flask']:
        raise ValueError("Không nhận diện được loại ứng dụng. Vui lòng đảm bảo project hợp lệ.")

    dockerfile_path = os.path.join(project_path, 'Dockerfile')

    with open(dockerfile_path, 'w', encoding='utf-8') as f:
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
            # Tự động tìm file chạy chính và thư mục cần set PYTHONPATH
            entrypoint, python_path = find_entrypoint_and_pythonpath(project_path)

            if not entrypoint or not python_path:
                raise Exception("❌ Không tìm thấy entrypoint hợp lệ trong dự án Flask.")

            # Ghi Dockerfile cho Flask
            f.write(f"""\
FROM python:3.11-slim
WORKDIR /{project_name}
COPY . .
ENV PYTHONPATH={f"/{python_path}" if python_path != "." else f"/{project_name}"}
RUN pip install python-dotenv
RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev
RUN pip install --no-cache-dir cryptography
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["sh", "-c", "sleep 15 && python {entrypoint}"]
""")




