from datetime import date

from app.extensions import db
from app.models.gauge import PressureGauge
from app.models.reminder import ReminderRecord


def run_reminder_scan():
    today = date.today()
    gauges = PressureGauge.query.all()
    created = []

    for gauge in gauges:
        remaining = (gauge.valid_until - today).days
        reminder_type = None
        if remaining == 30:
            reminder_type = "30d"
        elif remaining == 15:
            reminder_type = "15d"

        if not reminder_type:
            continue

        exists = ReminderRecord.query.filter_by(
            gauge_id=gauge.id,
            reminder_type=reminder_type,
        ).first()
        if exists:
            continue

        record = ReminderRecord(gauge_id=gauge.id, reminder_type=reminder_type)
        db.session.add(record)
        created.append(record)

    db.session.commit()
    return created


def get_pending_reminders():
    records = ReminderRecord.query.order_by(ReminderRecord.created_at.desc()).all()
    return [record.to_dict() for record in records]
