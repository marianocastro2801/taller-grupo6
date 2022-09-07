from sqlalchemy import Table, Column, ForeignKey
from app.db import db

rol_user = Table('roles_usuarios', db.metadata,
                 Column('rol_id', ForeignKey('roles.id'), primary_key=True),
                 Column('user_id', ForeignKey('usuarios.id'), primary_key=True)
                 )
