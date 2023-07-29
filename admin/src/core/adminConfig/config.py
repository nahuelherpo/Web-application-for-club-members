from datetime import datetime

from src.core.database import db


class Config(db.Model):
    """Modelo de la tabla de configuración."""

    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    cant_elementos = db.Column(db.Integer, nullable=False)
    pago_habilitado = db.Column(db.Boolean, nullable=False)
    info_contacto = db.Column(db.String(255), nullable=False)
    texto_recibo = db.Column(db.String(255), nullable=False)
    valor_cuota_base = db.Column(db.Numeric, nullable=False)
    porcentaje_recargo = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())
