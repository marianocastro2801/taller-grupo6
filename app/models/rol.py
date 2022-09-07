from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import db
from app.models.rol_permission import rol_permission
from app.models.rol_user import rol_user


class Rol(db.Model):

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=False, nullable=False)
    usuarios = relationship("User", secondary=rol_user, back_populates="roles")
    permisos = relationship("Permission", secondary=rol_permission)

    def __init__(self, nombre=None):
        self.nombre = nombre

    def __repr__(self):
        return "<Rol(nombre='%s')>" % (self.nombre)

    @classmethod
    def get_all_roles(self):
        return Rol.query.all()

    @staticmethod
    def get_by_id(id):
        return Rol.query.get(id)

    def __eq__(self, other):
       return self.nombre == other.nombre
