from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'admin.login'

    # Регистрация blueprints
    from .routes import main
    from .admin_routes import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')

    # Создание таблиц базы данных
    with app.app_context():
        db.create_all()

    return app