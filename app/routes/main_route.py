from flask import Blueprint, render_template,redirect,request,url_for,flash,session
from app import login_manager

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

@main_bp.route('/success')
def success():
    return render_template('success.html')