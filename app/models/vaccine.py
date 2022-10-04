from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class Vaccine(db.Model):
    __tablename__ = "vacunas"
    id = Column(Integer, primary_key=True)
    nombre_comercial = Column(String(50), unique=False, nullable=False)

    nombre_registro = Column(TINYTEXT, unique=False, nullable=False)

    enfermedad = Column(TINYTEXT, unique=False, nullable=False)
    
    desarrollador_id = Column(Integer, ForeignKey("vacuna_desarrollador.id"), nullable=False)
    desarrollador = relationship("VaccineDeveloper")

    tipo_id = Column(Integer, ForeignKey("vacuna_tipos.id"), nullable=False)
    tipo = relationship("VaccineType")


    cantidad = Column(Integer, unique=False, nullable=False)


    def __init__(self, nombre_comercial, nombre_registro, enfermedad, tipo_id, desarrollador_id,
    ):
        self.nombre_comercial = nombre_comercial
        self.nombre_registro = nombre_registro
        self.enfermedad = enfermedad
        self.tipo_id= tipo_id
        self.desarrollador_id = desarrollador_id
        self.cantidad = 0
       

    def __repr__(self):
        return "<Vaccine(nombre_comercial='%s', nombre_registro='%s', enfermedad='%s', )>" % (
            self.nombre_comercial,
            self.nombre_registro,
            self.enfermedad,

  
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def update():
        db.session.commit()


    @staticmethod
    def get_by_id(vaccine_id):
        with db.session.no_autoflush:
            return Vaccine.query.get(vaccine_id)


    @staticmethod
    def get_all_vaccines():
        return Vaccine.query.all()

    
    @staticmethod
    def update(**kwargs):
        vaccine = Vaccine.get_by_id(kwargs["id"])
        for key, value in kwargs.items():
            setattr(vaccine, key, value) 
        db.session.commit()
        
    @staticmethod
    def delete(vaccine_id):
        Vaccine.query.filter(Vaccine.id == vaccine_id).delete()
        db.session.commit()

    @staticmethod
    def get_filtered(search, type_id):
        return Vaccine.query.filter(Vaccine.nombre_comercial.ilike(f'%{search}%'), (Vaccine.tipo_id == type_id))
          

#   @classmethod
#   def get_vaccine_by_nombre_comercial(self, nombre_comercial):
#       return Vaccine.query.filter(self.nombre_comercial == nombre_comercial).first()

#   @classmethod
#   def nombre_comercial_esta_disponible(self, nombre_comercial):
#       return (self.get_vaccine_by_nombre_comercial(nombre_comercial)) == None