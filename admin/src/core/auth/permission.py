from datetime import datetime

from src.core.database import db


class Permission(db.Model):
    """Modelo de la tabla de permisos (create, delete, modify, list, etc)."""

    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
