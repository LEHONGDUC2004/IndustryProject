from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Khởi tạo đối tượng (global)
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Cấu hình ứng dụng
    app.config['SECRET_KEY'] = 'secret123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@db/upload_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo các extension
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # endpoint phải tồn tại (nên kiểm tra)

    # Đăng ký các blueprint (để sau khi app khởi tạo)
    from app.routes import register_routes
    register_routes(app)

    return app