from datetime import datetime

from src.core.database import db


role_permission = db.Table("rol_permission",
                           db.Column("role_id", db.Integer, db.ForeignKey(
                               "roles.id"), primary_key=True),
                           db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True))


class Role(db.Model):
    """Modelo de la tabla de roles (operadores, administradores)."""

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    permissions = db.relationship(
        "Permission", secondary=role_permission, backref="roles")
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
