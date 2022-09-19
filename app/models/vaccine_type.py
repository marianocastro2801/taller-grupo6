from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import db


class VaccineType(db.Model):
    __tablename__ = "vacuna_tipos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    vacunas = relationship("Vaccine", back_populates="tipo")

    def __repr__(self):
        return (
            self.nombre
        )

    @classmethod
    def get_all_types(self):
        return VaccineType.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineType.query.get(id)