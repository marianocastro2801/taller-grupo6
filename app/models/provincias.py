from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db import db


class Province(db.Model):
    __tablename__ = "provincias"
    id = Column(Integer, primary_key=True)
    nombre_provincia = Column(String(50), unique=True, nullable=False)
    


    def __repr__(self):
        return (
            self.nombre_provincia,

        )

    @classmethod
    def get_all_provincias(self):
        return Province.query.all()
        
    @staticmethod
    def get_by_id(id):
        return Province.query.get(id)