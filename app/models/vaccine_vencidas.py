from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db import db


class VaccineVencida(db. Model):
   __tablename__ = "vacunas_vencidas"
   id = Column(Integer, prymary_key = True)

   enfermedad_id = Column(Integer, ForeignKey("vacuna_enfermedad.id"), nullable=False)
   enfermedad = relationship("VaccineEnfermedad")

   provinci_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
   provincia = relationship("Province")

   cantidad= Column(Integer, unique=False, nullable=False)

   
   
   
   def __init__(self, enfermedad_id, provincia_id, cantidad
    ):
        
        self.enfermedad_id = enfermedad_id
        self.provincia_id = provincia_id
        self.cantidad = cantidad
       

   def __repr__(self):
       return "<VaccineVencida(cantidad='%s', )>" % (
           self.cantidad

       )

   @classmethod
   def get_all_vencidas(self):
       return VaccineVencida.query.all()
        
   @staticmethod
   def get_by_id(id):
       return VaccineVencida.query.get(id)


#SON REGLAS PREDEFINIDAS POR CALENDARIO