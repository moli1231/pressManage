import os

from flask import Flask

from app.blueprints.auth import auth_bp
from app.blueprints.files import files_bp
from app.blueprints.gauges import gauges_bp
from app.blueprints.health import health_bp
from app.blueprints.reminders import reminders_bp
from app.blueprints.users import users_bp
from app.config import config_map
from app.extensions import cors, db, jwt, migrate
from app.models import *  # noqa: F401,F403
from app.models.user import User, UserRole
from app.tasks.reminder_task import start_scheduler


def create_app(env: str | None = None):
    app = Flask(__name__)
    config_name = env or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_map.get(config_name, config_map["development"]))

    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1")
    app.register_blueprint(users_bp, url_prefix="/api/v1")
    app.register_blueprint(gauges_bp, url_prefix="/api/v1")
    app.register_blueprint(files_bp, url_prefix="/api/v1")
    app.register_blueprint(reminders_bp, url_prefix="/api/v1")

    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        _ensure_super_user(app)
        print("database initialized")

    @app.errorhandler(404)
    def not_found(_):
        return {"code": 404, "message": "not found", "data": {}}, 404

    @app.errorhandler(500)
    def server_error(_):
        return {"code": 500, "message": "internal server error", "data": {}}, 500

    if not app.debug:
        start_scheduler(app)

    with app.app_context():
        db.create_all()
        _ensure_super_user(app)

    return app


def _ensure_super_user(app):
    phone = os.getenv("INITIAL_SUPER_PHONE", "13800000000")
    password = os.getenv("INITIAL_SUPER_PASSWORD", "Admin@123")
    existing = User.query.filter_by(phone=phone).first()
    if existing:
        return

    user = User(phone=phone, role=UserRole.SUPER.value)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    app.logger.info("initial super user created: %s", phone)
