from app.extensions import db
from app.models.base import TimestampMixin


class ImportExportLog(TimestampMixin, db.Model):
    __tablename__ = "import_export_logs"

    id = db.Column(db.Integer, primary_key=True)
    op_type = db.Column(db.String(20), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    operator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    result = db.Column(db.String(255), nullable=False)
