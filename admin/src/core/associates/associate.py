from datetime import datetime
import enum

from src.core.database import db


associate_discipline = db.Table("associate_discipline",
                                db.Column("associate_id", db.Integer, db.ForeignKey(
                                    "associates.id"), primary_key=True),
                                db.Column("discipline_id", db.Integer, db.ForeignKey("disciplines.id"), primary_key=True))


class DocumentTypeEnum(enum.Enum):
    dni = "Documento Nacional de Identidad"
    lc = "Libreta Cívica"
    le = "Libreta de Enrolamiento"
    ci = "Cédula de identidad"


class GenderEnum(enum.Enum):
    f = "Femenino"
    m = "Masculino"
    otro = "Otro"


class Associate(db.Model):
    """Modelo de la tabla de asociados."""

    __tablename__ = "associates"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    document_type = db.Column(
        db.Enum(DocumentTypeEnum), default=DocumentTypeEnum.dni, nullable=False)
    document_number = db.Column(db.String(8), nullable=False, unique=True)
    gender = db.Column(db.Enum(GenderEnum),
                       default=GenderEnum.otro, nullable=False)
    address = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False) 
    card_issue_date = db.Column(db.DateTime, nullable=True, default=None)
    fees = db.relationship('Fee', backref='associate')
    date_of_birth = db.Column(db.DateTime)
    disciplines_practiced = db.relationship(
        "Discipline", secondary=associate_discipline, backref="associates_enrolled")
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.Date, default=datetime.now())

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'document_type': self.document_type.value,
            'document_number': self.document_number,
            'gender': self.gender.value,
            'address': self.address,
            'status': self.status,
            'phone_number': self.phone_number,
            'email': self.email
        }
