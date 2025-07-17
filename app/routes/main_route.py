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