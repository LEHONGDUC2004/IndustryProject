from flask import Blueprint, render_template, request, Response
import requests, logging

jenkins_bp = Blueprint('jenkins_view', __name__)
logger = logging.getLogger(__name__)

# Jenkins config
JENKINS_BASE_URL = 'http://3.212.74.20:8080'
JENKINS_JOB_URL = f"{JENKINS_BASE_URL}/job/build-web-static/buildWithParameters"
JENKINS_VIEW_URL = f"{JENKINS_BASE_URL}/view/MyView"
JENKINS_USER = 'lehongduc3491'
JENKINS_API_TOKEN = '11e592530e49b4dde7bdf44ee65b6e9685'


# Trigger build with ZIP_NAME param
def trigger_jenkins_build(zip_filename):
    payload = {
        'ZIP_NAME': zip_filename
    }
    response = requests.post(
        JENKINS_JOB_URL,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        params=payload
    )
    logger.info(f"Triggered Jenkins build with ZIP_NAME={zip_filename}, status={response.status_code}")
    return response.status_code


# Thêm route để hiển thị trang có iframe Jenkins
@jenkins_bp.route('/jenkins-dashboard')
def jenkins_dashboard():
    return render_template('jenkins_dashboard.html')


# Thêm route proxy để bypass X-Frame-Options
@jenkins_bp.route('/jenkins-proxy/<path:jenkins_path>')
def jenkins_proxy(jenkins_path):
    # Xây dựng URL hoàn chỉnh để truy cập Jenkins
    url = f"{JENKINS_BASE_URL}/{jenkins_path}"

    # Chuyển tiếp request đến Jenkins
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        auth=(JENKINS_USER, JENKINS_API_TOKEN),
        allow_redirects=False
    )

    # Tạo response và loại bỏ headers ngăn chặn iframe
    response = Response(resp.content)
    for name, value in resp.headers.items():
        if name.lower() not in ['x-frame-options', 'content-security-policy']:
            response.headers[name] = value

    return response


# Thêm route trực tiếp đến MyView (tùy chọn)
@jenkins_bp.route('/jenkins-view')
def jenkins_view():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jenkins MyView</title>
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; }}
            iframe {{ width: 100%; height: 100vh; border: none; }}
        </style>
    </head>
    <body>
        <iframe src="/jenkins-proxy/view/MyView/"></iframe>
    </body>
    </html>
    """