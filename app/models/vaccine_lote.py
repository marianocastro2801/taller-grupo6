from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db import db


class VaccineLote(db.Model):
    __tablename__ = "vacuna_lotes"
    id = Column(Integer, primary_key=True)
    nombre_lote = Column(String(50), unique=True, nullable=False)
  
    fecha_vencimiento = Column(Date, unique=False, nullable=False)
    compras = relationship("Shopping", back_populates="lote")

    def __repr__(self):
        return (
            self.nombre_lote,
            self.fecha_vencimiento
        )

    @classmethod
    def get_all_lotes(self):
        return VaccineLote.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineLote.query.get(id)