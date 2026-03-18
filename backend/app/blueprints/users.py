from flask import Blueprint, request

from app.extensions import db
from app.models.user import User, UserRole
from app.utils.auth import require_roles
from app.utils.response import fail, success

users_bp = Blueprint("users", __name__)


@users_bp.post("/users")
@require_roles(UserRole.ADMIN, UserRole.SUPER)
def create_user():
    data = request.get_json() or {}
    phone = str(data.get("phone", "")).strip()
    password = str(data.get("password", "")).strip()
    role = str(data.get("role", "user")).strip()

    if role not in {UserRole.USER.value, UserRole.SUPER.value}:
        return fail("只能创建普通用户或超级用户")
    if not phone or not password:
        return fail("手机号和密码必填")
    if User.query.filter_by(phone=phone).first():
        return fail("手机号已存在")

    user = User(phone=phone, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return success(user.to_dict(), "创建成功")


@users_bp.get("/users")
@require_roles(UserRole.ADMIN, UserRole.SUPER)
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return success({"items": [user.to_dict() for user in users], "total": len(users)})


@users_bp.patch("/users/<int:user_id>/status")
@require_roles(UserRole.ADMIN, UserRole.SUPER)
def update_status(user_id: int):
    data = request.get_json() or {}
    is_active = data.get("is_active", True)
    if isinstance(is_active, str):
        is_active = is_active.lower() in {"true", "1", "yes"}
    else:
        is_active = bool(is_active)
    user = User.query.get_or_404(user_id)
    user.is_active = is_active
    db.session.commit()
    return success(user.to_dict(), "状态更新成功")
