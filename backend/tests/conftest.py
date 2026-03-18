import pytest

from app import create_app
from app.extensions import db
from app.models.user import User, UserRole


@pytest.fixture()
def app():
    app = create_app("development")
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(phone="13900000000", role=UserRole.ADMIN.value)
        admin.set_password("Admin@123")
        super_user = User(phone="13700000000", role=UserRole.SUPER.value)
        super_user.set_password("Super@123")
        normal_user = User(phone="13600000000", role=UserRole.USER.value)
        normal_user.set_password("User@123")
        db.session.add_all([admin, super_user, normal_user])
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
