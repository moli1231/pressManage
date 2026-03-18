from datetime import datetime

from flask import Blueprint, request, send_file

from app.extensions import db
from app.models.gauge import GaugeType, PressureGauge
from app.services.excel_service import export_gauges_to_excel, import_gauges_from_excel
from app.utils.auth import get_current_user, require_roles
from app.utils.response import fail, success

gauges_bp = Blueprint("gauges", __name__)


@gauges_bp.get("/gauges")
@require_roles("user", "super", "admin")
def list_gauges():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    keyword = request.args.get("keyword", "").strip()

    query = PressureGauge.query
    if keyword:
        query = query.filter(PressureGauge.gauge_code.contains(keyword))

    pagination = query.order_by(PressureGauge.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return success(
        {
            "items": [item.to_dict() for item in pagination.items],
            "total": pagination.total,
            "page": page,
            "page_size": page_size,
        }
    )


@gauges_bp.get("/gauges/<int:gauge_id>")
@require_roles("user", "super", "admin")
def get_gauge(gauge_id: int):
    gauge = PressureGauge.query.get_or_404(gauge_id)
    return success(gauge.to_dict())


@gauges_bp.post("/gauges")
@require_roles("super")
def create_gauge():
    payload = request.get_json() or {}
    check = _validate_payload(payload)
    if check:
        return check

    current_user = get_current_user()
    if PressureGauge.query.filter_by(gauge_code=payload["gauge_code"]).first():
        return fail("压力表编号已存在")

    gauge = PressureGauge(
        gauge_code=payload["gauge_code"],
        inspection_days=int(payload["inspection_days"]),
        manufacturer=payload["manufacturer"],
        serial_no=payload["serial_no"],
        location=payload["location"],
        entity_photo_path=payload.get("entity_photo_path"),
        report_photo_path=payload.get("report_photo_path"),
        calibration_date=datetime.strptime(payload["calibration_date"], "%Y-%m-%d").date(),
        gauge_type=payload["gauge_type"],
        created_by=current_user.id,
    )
    db.session.add(gauge)
    db.session.commit()
    return success(gauge.to_dict(), "创建成功")


@gauges_bp.put("/gauges/<int:gauge_id>")
@require_roles("super")
def update_gauge(gauge_id: int):
    payload = request.get_json() or {}
    check = _validate_payload(payload, update=True)
    if check:
        return check

    gauge = PressureGauge.query.get_or_404(gauge_id)
    if "gauge_code" in payload:
        exists = PressureGauge.query.filter(
            PressureGauge.gauge_code == payload["gauge_code"],
            PressureGauge.id != gauge_id,
        ).first()
        if exists:
            return fail("压力表编号已存在")

    for field in [
        "gauge_code",
        "inspection_days",
        "manufacturer",
        "serial_no",
        "location",
        "entity_photo_path",
        "report_photo_path",
        "gauge_type",
    ]:
        if field in payload:
            setattr(gauge, field, payload[field])

    if "calibration_date" in payload:
        gauge.calibration_date = datetime.strptime(payload["calibration_date"], "%Y-%m-%d").date()

    db.session.commit()
    return success(gauge.to_dict(), "更新成功")


@gauges_bp.delete("/gauges/<int:gauge_id>")
@require_roles("super")
def delete_gauge(gauge_id: int):
    gauge = PressureGauge.query.get_or_404(gauge_id)
    db.session.delete(gauge)
    db.session.commit()
    return success(message="删除成功")


@gauges_bp.post("/gauges/import")
@require_roles("super")
def import_gauges():
    upload = request.files.get("file")
    if not upload:
        return fail("请上传 Excel 文件")

    user = get_current_user()
    result = import_gauges_from_excel(upload.stream, user.id)
    return success(result)


@gauges_bp.get("/gauges/export")
@require_roles("super", "admin")
def export_gauges():
    gauges = PressureGauge.query.order_by(PressureGauge.created_at.desc()).all()
    output = export_gauges_to_excel(gauges)
    filename = f"gauges-{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def _validate_payload(payload: dict, update=False):
    required = ["gauge_code", "inspection_days", "manufacturer", "serial_no", "location", "calibration_date", "gauge_type"]

    if not update:
        for field in required:
            if field not in payload or payload[field] in [None, ""]:
                return fail(f"{field} 为必填项")

    if "gauge_type" in payload and payload["gauge_type"] not in {
        GaugeType.ELECTRONIC.value,
        GaugeType.MECHANICAL.value,
    }:
        return fail("压力表类型无效")

    if "inspection_days" in payload:
        try:
            days = int(payload["inspection_days"])
            if days <= 0:
                return fail("inspection_days 必须大于 0")
        except Exception:
            return fail("inspection_days 必须是整数")

    if "calibration_date" in payload:
        try:
            datetime.strptime(payload["calibration_date"], "%Y-%m-%d")
        except Exception:
            return fail("calibration_date 格式必须为 YYYY-MM-DD")

    return None
