from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class VaccineDeveloper(db.Model):
    __tablename__ = "vacuna_desarrollador"
    id = Column(Integer, primary_key=True)
    nombre_desarrollador = Column(TINYTEXT, unique=False, nullable=False)
    vacunas = relationship("Vaccine", back_populates="desarrollador")

    def __repr__(self):
        return (
            self.nombre_desarrollador
        )

    @classmethod
    def get_all_desarrolladores(self):
        return VaccineDeveloper.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineDeveloper.query.get(id)