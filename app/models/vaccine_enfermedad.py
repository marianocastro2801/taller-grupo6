from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db import db


class VaccineEnfermedad(db.Model):
    __tablename__ = "vacuna_enfermedad"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    vacunas = relationship("Vaccine", back_populates="enfermedad")
    fecha_inicio = Column(Date, unique=False, nullable=False)
    fecha_fin = Column(Date, unique=False, nullable=False)
    
    def __repr__(self):
        return (
            self.nombre
        )

    @classmethod
    def get_all_enfermedades(self):
        return VaccineEnfermedad.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineEnfermedad.query.get(id)