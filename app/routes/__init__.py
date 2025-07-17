from app.routes.main_route import main_bp
from app.routes.upload import upload_bp

def register_routes(app):
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(upload_bp, url_prefix='/upload')
