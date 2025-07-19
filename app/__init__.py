from flask import Flask
from app.extensions import db, login_manager
from app.models import Account


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@db/upload_app?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # đăng ký user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return Account.query.get(int(user_id))

    from app.routes import register_routes
    register_routes(app)
    with app.app_context():
        db.create_all()

    return app