from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import db


class VaccineLote(db.Model):
    __tablename__ = "vacuna_lotes"
    id = Column(Integer, primary_key=True)
    nombre_lote = Column(String(50), unique=True, nullable=False)
    vacunas = relationship("Vaccine", back_populates="lote")

    def __repr__(self):
        return (
            self.nombre_lote
        )

    @classmethod
    def get_all_lotes(self):
        return VaccineLote.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineLote.query.get(id)