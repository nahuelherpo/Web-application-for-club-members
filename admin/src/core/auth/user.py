from datetime import datetime

from src.core.database import db


user_rol = db.Table("user_rol",
                    db.Column("user_id", db.Integer, db.ForeignKey(
                        "users.id"), primary_key=True),
                    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True))


class User(db.Model):
    """Modelo de la tabla de usuarios (operadores, administradores)."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # hash
    active = db.Column(db.Boolean, nullable=False, default=True)
    roles = db.relationship("Role", secondary=user_rol,
                            backref="users_with_role")
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
