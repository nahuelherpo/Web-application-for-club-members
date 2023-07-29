from datetime import datetime

from src.core.database import db


class Fee(db.Model):
    """Modelo de la clase cuota."""

    __tablename__ = "fees"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    expiration_date = db.Column(db.Date, nullable=False)
    amount_to_pay = db.Column(db.Float, nullable=False)
    associate_id = db.Column(db.Integer, db.ForeignKey(
        'associates.id'), nullable=False)  # A quien le corresponde la cuota
    receipt = db.relationship("Receipt", back_populates="fee", uselist=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
    __table_args__ = (db.CheckConstraint((month >= 1) & (month <= 12), name="check_valid_month"),
                      {})
