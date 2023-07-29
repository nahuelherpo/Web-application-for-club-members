from datetime import datetime

from src.core.database import db


class Category(db.Model):
    """Modelo de la tabla de categoria."""

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # año categoria, deporte, etc.
    name = db.Column(db.String(100), nullable=False)
    instructors = db.Column(db.String(150), nullable=False)
    days = db.Column(db.String(50))  # Lunes y miercoles
    hour_fence = db.Column(db.String(50))  # 14hs a 16hs
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
