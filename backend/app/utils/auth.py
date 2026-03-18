from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models.user import User, UserRole
from app.utils.response import fail


def require_roles(*roles: UserRole):
    allowed = {role.value if isinstance(role, UserRole) else str(role) for role in roles}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = User.query.get(int(identity))
            if not user or not user.is_active:
                return fail("账号不可用", status_code=403)
            if allowed and user.role not in allowed:
                return fail("权限不足", status_code=403)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_current_user():
    verify_jwt_in_request()
    identity = get_jwt_identity()
    return User.query.get(int(identity))
