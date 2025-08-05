from flask import Blueprint, render_template,redirect,request,url_for,flash,session
from app import login_manager
from flask import request, render_template
import requests

main_bp = Blueprint('main', __name__)

login_manager.login_view = 'main.login'

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/upload_code')
def upload_code():
    return render_template('upload_code.html')

@main_bp.route('/deploy_code')
def deploy_code():
    return render_template('deploy.html')

@main_bp.route('/upload_infodb')
def upload_infodb():
    return render_template('upload/info_db.html')

@main_bp.route("/success")
def success():
    zip_name = request.args.get("zip_name")
    jobs_info = []

    if not zip_name:
        return render_template("success.html", jobs=[])

    # Lấy danh sách job trong view MyView
    response = requests.get(
        "http://3.212.74.20:8080/view/MyView/api/json?tree=jobs[name,url,color]",
        auth=('lehongduc3491', '11e592530e49b4dde7bdf44ee65b6e9685')
    )

    for job in response.json().get("jobs", []):
        # Gọi API để lấy thông tin build gần nhất
        build_resp = requests.get(f"{job['url']}lastBuild/api/json", auth=('lehongduc3491', '11e592530e49b4dde7bdf44ee65b6e9685'))
        build_data = build_resp.json()

        # Kiểm tra nếu có tham số zip_name trong build
        actions = build_data.get("actions", [])
        for act in actions:
            if "parameters" in act:
                for p in act["parameters"]:
                    if p["name"] == "ZIP_NAME" and p["value"] == zip_name:
                        jobs_info.append({
                            "name": job["name"],
                            "url": job["url"],
                            "build_url": build_data.get("url"),
                            "result": build_data.get("result"),
                            "timestamp": build_data.get("timestamp")
                        })

    return render_template("success.html", jobs=jobs_info)