from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

# Khởi tạo các extension của Flask
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """
    Application Factory: Khởi tạo và cấu hình ứng dụng Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Đăng ký các extension với instance ứng dụng
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Cấu hình Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục thao tác.'
    login_manager.login_message_category = 'warning'

    # Đăng ký blueprint chính
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
