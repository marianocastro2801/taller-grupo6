from sqlalchemy import Column, Integer, String
from app.db import db


class Permission(db.Model):

    __tablename__ = "permisos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=False, nullable=False)

    def __init__(self, nombre=None):
        self.nombre = nombre

    def __repr__(self):
        return "<Permission(nombre='%s')>" % (self.nombre)
