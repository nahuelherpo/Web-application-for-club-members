from datetime import datetime

from src.core.database import db


class Receipt(db.Model):
    """Modelo de la clase recibo."""

    __tablename__ = "receipts"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    payment_date = db.Column(db.DateTime)
    amount_paid = db.Column(db.Float)
    paid_by = db.Column(db.String(60))
    fee_id = db.Column(db.Integer, db.ForeignKey("fees.id"))
    fee = db.relationship("Fee", back_populates="receipt")
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
    __table_args__ = (db.CheckConstraint(amount_paid > 0, name='check_amount_positive'),
                      {})
