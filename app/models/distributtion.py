from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class Distributtion(db.Model):
    __tablename__ = "distribuciones"
    id = Column(Integer, primary_key=True)

    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    vacuna = relationship("Vaccine")

    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship("Province")

    cantidad = Column(Integer, unique=False, nullable=False)


    def __init__(self, vacuna_id, provincia_id, cantidad
    ):
        self.vacuna_id= vacuna_id
        self.provincia_id = provincia_id
        self.cantidad = cantidad
       

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
  