from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey, text, Date
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class Patient(db.Model):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True)
    dni = Column(String(50), unique=False, nullable=False)

    fecha_nacimiento = Column(Date, unique=False, nullable=False)



    def __init__(self, dni, fecha_nacimiento
    ):
        self.dni= dni
        self.fecha_nacimiento= fecha_nacimiento
   
       

    def __repr__(self):
        return "<Patient(dni='%s', fecha_nacimiento='%s', )>" % (
            self.dni,
            self.fecha_nacimiento,
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def update():
        db.session.commit()


    @staticmethod
    def get_by_id(patient_id):
        with db.session.no_autoflush:
            return Patient.query.get(patient_id)


    @staticmethod
    def get_all_pacientes():
        return Patient.query.all()

    
    @staticmethod
    def update(**kwargs):
        patient = Patient.get_by_id(kwargs["id"])
        for key, value in kwargs.items():
            setattr(patient, key, value) 
        db.session.commit()
        
    @staticmethod
    def delete(patient_id):
        Patient.query.filter(Patient.id == patient_id).delete()
        db.session.commit()

    