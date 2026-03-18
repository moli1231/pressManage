import os
import uuid
from pathlib import Path

from flask import Blueprint, current_app, request, send_from_directory

from app.utils.auth import require_roles
from app.utils.response import fail, success

files_bp = Blueprint("files", __name__)

ALLOWED_SUFFIX = {".jpg", ".jpeg", ".png", ".webp"}


@files_bp.post("/files/upload")
@require_roles("super")
def upload_file():
    upload = request.files.get("file")
    if not upload:
        return fail("文件不能为空")

    ext = Path(upload.filename).suffix.lower()
    if ext not in ALLOWED_SUFFIX:
        return fail("仅支持 jpg/jpeg/png/webp")

    upload_dir = current_app.config["UPLOAD_DIR"]
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    abs_path = Path(upload_dir) / filename
    upload.save(abs_path)

    return success({"path": f"/uploads/{filename}", "filename": filename})


@files_bp.get("/uploads/<path:filename>")
def get_upload(filename):
    upload_dir = current_app.config["UPLOAD_DIR"]
    return send_from_directory(upload_dir, filename)
