from turtle import back
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db import db


class VacunattionApi(db.Model):
    __tablename__ = "vacunaciones_api"
    id = Column(Integer, primary_key=True)
    
    #datos api
    dni = Column(Integer, unique=False, nullable=False)
    nombre = Column(String(50), unique=True, nullable=False)
    apellido = Column(String(50), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, unique=False, nullable=False)
    
    
    enfermedad_id = Column(Integer, ForeignKey("vacuna_enfermedad.id"), nullable=False)
    enfermedad = relationship("VaccineEnfermedad")

    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship("Province")

   
    fecha_vacunacion = Column(Date, unique=False, nullable=False)


    def __repr__(self):
        return (
            self.dni
            
        )

    @classmethod
    def get_all_stocks(self):
        return VacunattionApi.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VacunattionApi.query.get(id)


    def save(self):
        db.session.add(self)
        db.session.commit()