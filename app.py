import os
import zipfile
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.secret_key = 'secret'  # dùng tạm cho flash message
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def generate_dockerfile(path):
    dockerfile_content = """\
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
"""
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'codezip' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['codezip']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            extract_folder = os.path.join(app.config['UPLOAD_FOLDER'], filename[:-4])
            os.makedirs(extract_folder, exist_ok=True)

            extract_zip(save_path, extract_folder)
            generate_dockerfile(extract_folder)

            flash(f'Uploaded and generated Dockerfile in: {extract_folder}')
            return redirect('/')

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
