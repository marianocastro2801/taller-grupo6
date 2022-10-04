from turtle import back
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import db


class VaccineStock(db.Model):
    __tablename__ = "vacuna_stock"
    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, unique=False, nullable=False)
    compras = relationship("Shopping")


    def __repr__(self):
        return (
            self.cantidad
        )

    @classmethod
    def get_all_stocks(self):
        return VaccineStock.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineStock.query.get(id)