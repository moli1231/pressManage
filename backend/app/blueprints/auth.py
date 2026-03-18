from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User
from app.utils.auth import get_current_user, require_roles
from app.utils.response import fail, success

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/auth/login")
def login():
    data = request.get_json() or {}
    phone = str(data.get("phone", "")).strip()
    password = str(data.get("password", "")).strip()

    if not phone or not password:
        return fail("手机号和密码必填")

    user = User.query.filter_by(phone=phone).first()
    if not user or not user.check_password(password):
        return fail("手机号或密码错误", status_code=401)
    if not user.is_active:
        return fail("账号已禁用", status_code=403)

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return success({"token": token, "user": user.to_dict()})


@auth_bp.post("/auth/change-password")
@require_roles("user", "admin", "super")
def change_password():
    user = get_current_user()
    data = request.get_json() or {}
    old_password = str(data.get("old_password", ""))
    new_password = str(data.get("new_password", ""))

    if not user.check_password(old_password):
        return fail("旧密码错误", status_code=400)
    if len(new_password) < 6:
        return fail("新密码至少 6 位")

    user.set_password(new_password)
    db.session.commit()
    return success(message="密码修改成功")


@auth_bp.post("/auth/logout")
@require_roles("user", "admin", "super")
def logout():
    return success(message="退出成功")
