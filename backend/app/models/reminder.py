from app.extensions import db
from app.models.base import TimestampMixin


class ReminderRecord(TimestampMixin, db.Model):
    __tablename__ = "reminder_records"

    id = db.Column(db.Integer, primary_key=True)
    gauge_id = db.Column(db.Integer, db.ForeignKey("pressure_gauges.id"), nullable=False)
    reminder_type = db.Column(db.String(10), nullable=False)
    sent_to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    __table_args__ = (db.UniqueConstraint("gauge_id", "reminder_type", name="uq_gauge_reminder"),)

    def to_dict(self):
        return {
            "id": self.id,
            "gauge_id": self.gauge_id,
            "reminder_type": self.reminder_type,
            "sent_to_user_id": self.sent_to_user_id,
            "sent_at": self.created_at.isoformat() if self.created_at else None,
        }
