from sqlalchemy import Table, Column, ForeignKey
from app.db import db

rol_permission = Table('roles_permisos', db.metadata,
                       Column('rol_id', ForeignKey('roles.id'), primary_key=True),
                       Column('permiso_id', ForeignKey('permisos.id'), primary_key=True)
                       )
