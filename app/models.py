
from flask_login import UserMixin
from app.extensions import db

class Account(db.Model, UserMixin):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    name_account = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Account {self.name_account}>"
#
# class Project(db.Model):
#     __tablename__ = 'project'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     repo_url = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#
#     deployments = db.relationship('Deployment', backref='project', lazy=True)
#     webhook_logs = db.relationship('WebhookLog', backref='project', lazy=True)
#     domains = db.relationship('Domain', backref='project', lazy=True)
#     env_vars = db.relationship('EnvironmentVariable', backref='project', lazy=True)
#
# class Deployment(db.Model):
#     __tablename__ = 'deployment'
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
#     zip_filename = db.Column(db.String(255))
#     status = db.Column(db.String(50), default='pending')  # pending, success, failed
#     logs = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#
# class WebhookLog(db.Model):
#     __tablename__ = 'webhook_log'
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
#     payload = db.Column(db.Text)
#     received_at = db.Column(db.DateTime, default=datetime.utcnow)
#
# class Domain(db.Model):
#     __tablename__ = 'domain'
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
#     domain = db.Column(db.String(255), unique=True)
#     verified = db.Column(db.Boolean, default=False)
#
# class EnvironmentVariable(db.Model):
#     __tablename__ = 'environment_variable'
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
#     key = db.Column(db.String(100))
#     value = db.Column(db.String(500))
#     is_secret = db.Column(db.Boolean, default=True)