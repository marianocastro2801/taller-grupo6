from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, delete, insert, update, text
from sqlalchemy.orm import relationship
from app.db import db
from app.models.rol_user import rol_user
from app.models.rol import Rol


class User(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    usrname = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=False, nullable=False)
    nombre = Column(String(50), unique=False, nullable=False)
    apellido = Column(String(50), unique=False, nullable=False)
    activo = Column(Boolean, unique=False, nullable=False)
    roles = relationship("Rol", secondary=rol_user, back_populates="usuarios")
    baja = Column(Boolean, unique=False, nullable=False)

    def __init__(
            self, email=None, usrname=None, password=None, nombre=None, apellido=None
    ):
        self.email = ((email),)
        self.usrname = ((usrname),)
        self.password = ((password),)
        self.nombre = ((nombre),)
        self.apellido = ((apellido),)
        self.activo = 1
        self.baja = 0
        self.roles = []

    def __repr__(self):
        return "<User(email='%s', usrname='%s', nombre='%s', apellido='%s', )>" % (
            self.email,
            self.usrname,
            self.nombre,
            self.apellido,
        )

    @staticmethod
    def get_by_id(id):
        with db.session.no_autoflush:
            return User.query.get(id)

    @classmethod
    def get_user_by_email_and_password(self, email, password):
        return User.query.filter(self.email == email, self.password == password).first()

    @classmethod
    def get_user_by_email(self, email):
        return User.query.filter(self.email == email).first()

    @classmethod
    def get_user_by_usrname(self, usrname):
        return User.query.filter(self.usrname == usrname).first()

    @classmethod
    def mail_esta_disponible(self, email):
        return (self.get_user_by_email(email)) == None

    @classmethod
    def usrname_esta_disponible(self, usrname):
        return (self.get_user_by_usrname(usrname)) == None

    @staticmethod
    def get_all_users():
        return User.query.all()
        
    @staticmethod
    def get_filtered(search):
        return User.query.filter(User.nombre.ilike(f'%{search}%'))

    def get_relevant_data(self):
        rols = set()
        for rol in self.roles:
            rols.add(rol.nombre)

        return {
            "id": self.id,
            "email": self.email,
            "usrname": self.usrname,
            "first_name": self.nombre,
            "last_name": self.apellido,
            "rols": rols
        }

    def is_valid(self):
        return self.activo and not self.baja

    def get_permissions(self):
        permissions = set()
        for rol in self.roles:
            for permission in rol.permisos:
                permissions.add(permission.nombre)
        return permissions

    def save(self, roles=None):
        if not self.id:
            if (roles != None):
                self.addRoles(roles)
            db.session.add(self)
            db.session.commit()

    def update(self, roles=None):
        usuario = User.get_by_id(self.id)
        usuario.updateFields(self)
        if (roles != None):
            usuario.addRoles(roles)
        db.session.commit()

    def activate(self):
        self.activo = 1
        db.session.commit()

    def deactivate(self):
        self.activo = 0
        db.session.commit()

    def remove(self):
        # db.session.delete(self)
        self.baja = 1
        db.session.commit()

    def updateFields(self, new):
        self.nombre = new.nombre
        self.email = new.email
        self.usrname = new.usrname
        self.apellido = new.apellido

    def addRoles(self, roles):
        self.roles.clear()
        for idRol in roles:
            self.roles.append(Rol.get_by_id(idRol))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    