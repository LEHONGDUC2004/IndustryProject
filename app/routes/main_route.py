from flask import Blueprint, render_template,redirect,request,url_for,flash,session
from app import login_manager
from flask_login import login_required,logout_user,current_user

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
    name_user=request.args.get('name','Khách')
    return render_template('indexLogin.html',name_user=current_user.name_account)

@main_bp.route('/logout')
def logout_process():
    return redirect(url_for('main.index'))

@main_bp.route('/passwd')
def setting_passwd():
    return render_template('setting/passwd.html',name_user=current_user.name_account)
