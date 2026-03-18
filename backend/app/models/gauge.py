from datetime import date, timedelta
from enum import Enum

from app.extensions import db
from app.models.base import TimestampMixin


class GaugeType(str, Enum):
    ELECTRONIC = "electronic"
    MECHANICAL = "mechanical"


class PressureGauge(TimestampMixin, db.Model):
    __tablename__ = "pressure_gauges"

    id = db.Column(db.Integer, primary_key=True)
    gauge_code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    inspection_days = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(120), nullable=False)
    serial_no = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    entity_photo_path = db.Column(db.String(255), nullable=True)
    report_photo_path = db.Column(db.String(255), nullable=True)
    calibration_date = db.Column(db.Date, nullable=False)
    valid_until = db.Column(db.Date, nullable=False)
    gauge_type = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def recompute_valid_until(self):
        self.valid_until = self.calibration_date + timedelta(days=self.inspection_days)

    @property
    def remaining_days(self):
        today = date.today()
        return (self.valid_until - today).days

    @property
    def expiry_status(self):
        if self.remaining_days < 0:
            return "expired"
        if self.remaining_days == 0:
            return "expires_today"
        return "active"

    def to_dict(self):
        return {
            "id": self.id,
            "gauge_code": self.gauge_code,
            "inspection_days": self.inspection_days,
            "manufacturer": self.manufacturer,
            "serial_no": self.serial_no,
            "location": self.location,
            "entity_photo_path": self.entity_photo_path,
            "report_photo_path": self.report_photo_path,
            "calibration_date": self.calibration_date.isoformat() if self.calibration_date else None,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "gauge_type": self.gauge_type,
            "created_by": self.created_by,
            "remaining_days": self.remaining_days,
            "expiry_status": self.expiry_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@db.event.listens_for(PressureGauge, "before_insert")
@db.event.listens_for(PressureGauge, "before_update")
def _sync_valid_until(mapper, connection, target: PressureGauge):
    if target.calibration_date and target.inspection_days is not None:
        target.valid_until = target.calibration_date + timedelta(days=target.inspection_days)
