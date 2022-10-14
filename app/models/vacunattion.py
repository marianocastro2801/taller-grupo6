from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db import db


class Vacunattion(db.Model):
    __tablename__ = "vacunaciones"
    id = Column(Integer, primary_key=True)
    fecha_vacunacion = Column(Date, unique=True, nullable=False)
    

    def __init__(self, fecha_vacunacion
    ):
        self.fecha_vacunacion= fecha_vacunacion
        

    def __repr__(self):
        return (
            self.fecha_vacunacion,

        )

    @classmethod
    def get_all_vacunaciones(self):
        return Vacunattion.query.all()
        
    @staticmethod
    def get_by_id(id):
        return Vacunattion.query.get(id)