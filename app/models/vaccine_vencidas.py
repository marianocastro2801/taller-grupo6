from sqlalchemy import Column, Integer, String, Date 
from sqlalchemy.orm import relationship
from app.db import db


class VaccineVencida(db.Model):
    __tablename__ = "vacunas_vencidas"
    id = Column(Integer, primary_key=True)
    
    enfermedad = Column(String(50), unique=True, nullable=False)
    provincia = Column(String(50), unique=True, nullable=False)
    cantidad= Column(Integer, unique=False, nullable=False)
    

    def __repr__(self):
        return (
            self.enfermedad
        )

    @classmethod
    def get_all_vencidas(self):
        return VaccineVencida.query.all()
        
    @staticmethod
    def get_by_id(id):
        return VaccineVencida.query.get(id)


#SON REGLAS PREDEFINIDAS POR CALENDARIO 