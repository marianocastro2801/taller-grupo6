from sqlalchemy import Column, Integer, String, Date 
from sqlalchemy.orm import relationship
from app.db import db


class VacunattionRegla(db.Model):
    __tablename__ = "vacunacion_reglas"
    id = Column(Integer, primary_key=True)
    
    enfermedad = Column(String(50), unique=True, nullable=False)
    numero_dosis= Column(Integer, unique=False, nullable=False)
    fecha_vacunacion = Column(Date, unique=True, nullable=False)

    def __repr__(self):
        return (
            self.enfermedad
        )

    @classmethod
    def get_all_types(self):
        return VacunattionRegla.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VacunattionRegla.query.get(id)


#SON REGLAS PREDEFINIDAS POR CALENDARIO 