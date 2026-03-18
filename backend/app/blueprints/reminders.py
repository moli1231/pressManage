from flask import Blueprint

from app.services.reminder_service import get_pending_reminders, run_reminder_scan
from app.utils.auth import require_roles
from app.utils.response import success

reminders_bp = Blueprint("reminders", __name__)


@reminders_bp.get("/reminders/pending")
@require_roles("admin", "super")
def pending_reminders():
    items = get_pending_reminders()
    return success({"items": items, "total": len(items)})


@reminders_bp.post("/reminders/run")
@require_roles("admin", "super")
def run_reminders():
    created = run_reminder_scan()
    return success({"created": [item.to_dict() for item in created], "count": len(created)})
