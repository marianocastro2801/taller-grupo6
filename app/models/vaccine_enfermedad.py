from asyncio.windows_events import NULL
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class VaccineEnfermedad(db.Model):
    __tablename__ = "vacuna_enfermedad"
    id = Column(Integer, primary_key=True)
    nombre = Column(TINYTEXT, unique=True, nullable=False)
    vacunas = relationship("Vaccine", back_populates="enfermedad")
    fecha_inicio = Column(Date, unique=False, nullable=False)
    fecha_fin = Column(Date, unique=False, nullable=False)
    
    def __init__(self, nombre, fecha_inicio, fecha_fin):
        self.nombre = nombre
 
        if fecha_inicio=='':
            self.fecha_inicio = None
        if not fecha_fin=='':
            self.fecha_fin = None

    def __repr__(self):
       return "<VaccineEnfermedad(nombre='%s')>" % (
            self.nombre
        )


    @classmethod
    def get_all_enfermedades(self):
        return VaccineEnfermedad.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineEnfermedad.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()