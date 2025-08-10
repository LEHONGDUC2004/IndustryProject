import os
from flask import Blueprint, render_template, redirect, request, url_for, flash, session, jsonify
from flask_login import login_required, logout_user, current_user
from app import login_manager, db
from app.models import Deployment, WebhookLog
from app.controller.config import WEBHOOK_SECRET
main_bp = Blueprint('main', __name__)

login_manager.login_view = 'main.login'

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload_code')
def upload_code():
    return render_template('upload_code.html',name_user=current_user.name_account)

@main_bp.route('/deploy_code')
def deploy_code():
    return render_template('deploy.html',name_user=current_user.name_account)

@main_bp.route('/upload_infodb')
def upload_infodb():
    return render_template('upload/info_db.html',name_user=current_user.name_account)

@main_bp.route("/success")
@login_required
def success():
    jobs = session.get('jobs', [])
    return render_template("success.html", jobs=jobs,name_user=current_user.name_account)

@main_bp.route('/register')
def register():
    return render_template('register.html')

@main_bp.route('/verify')
def verify():
    return render_template('verify.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/indexLogin')
@login_required
def index_login():
    return render_template('indexLogin.html',name_user=current_user.name_account)

@main_bp.route('/logout')
def logout_process():
    return redirect(url_for('main.index'))

@main_bp.route('/passwd')
def setting_passwd():
    return render_template('setting/passwd.html',name_user=current_user.name_account)



@main_bp.route("/webhooks/jenkins", methods=["POST"])
def jenkins_webhook():
    if WEBHOOK_SECRET and request.headers.get("X-Webhook-Secret") != WEBHOOK_SECRET:
        return jsonify({"ok": False, "error": "forbidden"}), 403

    data = request.get_json(silent=True) or {}
    dep_id = data.get("deploy_id")
    status = (data.get("status") or "").upper()
    duration_ms = data.get("duration_ms") or 0

    if dep_id:
        dep = Deployment.query.get(dep_id)
        if dep:
            dep.status = "success" if status == "SUCCESS" else "failed"
            dep.build_time = float(duration_ms) / 1000.0
            db.session.add(dep)

            wl = WebhookLog(project_id=dep.project_id, payload=str(data))
            db.session.add(wl)
            db.session.commit()


    # dep.logs = get_full_log(data["job"], data["build_number"]); db.session.commit()

    return jsonify({"ok": True})

# Cho phép GET để health-check nhanh trên trình duyệt
@main_bp.route("/webhooks/jenkins", methods=["GET"])
def jenkins_webhook_health():
    return "Webhook OK. Use POST here.", 200
