from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class Distributtion(db.Model):
    __tablename__ = "distribuciones"
    id = Column(Integer, primary_key=True)

    enfermedad_id = Column(Integer, ForeignKey("vacuna_enfermedad.id"), nullable=False)
    enfermedad = relationship("VaccineEnfermedad")

    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship("Province")

    lote_id = Column(Integer, ForeignKey("vacuna_lotes.id"), nullable=False)
    lote = relationship("VaccineLote")

    cantidad = Column(Integer, unique=False, nullable=False)


    def __init__(self, provincia_id, enfermedad_id, lote_id, cantidad
    ):
        self.provincia_id = provincia_id
        self.cantidad = cantidad
        self.enfermedad_id = enfermedad_id
        self.lote_id = lote_id
       

    def __repr__(self):
        return "<Distributtion(cantidad='%s', )>" % (
            self.cantidad,

        )

    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def update():
        db.session.commit()


    @staticmethod
    def get_by_id(distributtion_id):
        with db.session.no_autoflush:
            return Distributtion.query.get(distributtion_id)


    @staticmethod
    def get_all_distributtiones():
        return Distributtion.query.all()

    @staticmethod
    def get_filtered(enfermedad_id):
   
        return Distributtion.query.filter(Distributtion.enfermedad_id == enfermedad_id) 
  
    @staticmethod
    def get_filtered_provincia(provincia_id):
   
        return Distributtion.query.filter(Distributtion.provincia_id == provincia_id) 