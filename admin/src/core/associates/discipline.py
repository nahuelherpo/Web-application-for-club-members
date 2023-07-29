from datetime import datetime

from src.core.database import db


discipline_category = db.Table("discipline_category",
                               db.Column("discipline_id", db.Integer, db.ForeignKey(
                                   "disciplines.id"), primary_key=True),
                               db.Column("category_id", db.Integer, db.ForeignKey("categories.id"), primary_key=True))


class Discipline(db.Model):

    """Modelo de la tabla de disciplinas."""

    __tablename__ = "disciplines"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    monthly_price = db.Column(db.Float)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    categories = db.relationship(
        "Category", secondary=discipline_category)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    inserted_at = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id
        }
