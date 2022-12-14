from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db import db


class Vacunattion(db.Model):
    __tablename__ = "vacunaciones"
    id = Column(Integer, primary_key=True)
    fecha_vacunacion = Column(Date, unique=True, nullable=False)

    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    paciente = relationship("Patient")

    enfermedad_id = Column(Integer, ForeignKey("vacuna_enfermedad.id"), nullable=False)
    enfermedad = relationship("VaccineEnfermedad")

    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship("Province")

    numero_dosis= Column(Integer, unique=False, nullable=False)
   

    def __init__(self, fecha_vacunacion, paciente_id, enfermedad_id, provincia_id, numero_dosis
    ):
        self.fecha_vacunacion= fecha_vacunacion
        self.paciente_id=paciente_id
        self.enfermedad_id = enfermedad_id
        self.provincia_id = provincia_id
        self.numero_dosis = numero_dosis
    

    def __repr__(self):
        return "<Vacunattion(fecha_vacunacion='%s', paciente_id='%s', enfermedad_id='%s', provincia_id='%s', numero_dosis='%s' )>" % (
            
            self.fecha_vacunacion,
            self.paciente_id,
            self.enfermedad_id,
            self.provincia_id,
             self.numero_dosis,

        )


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_vacunaciones(self):
        return Vacunattion.query.all()
        
    @staticmethod
    def get_by_id(id):
        return Vacunattion.query.get(id)

    @classmethod
    def get_vacunattiones_by_provincia(self, provincia_id):
        return Vacunattion.query.filter(self.provincia_id == provincia_id).all()

    @classmethod
    def get_vacunattiones_by_enfermedad(self, enfermedad_id):
        return Vacunattion.query.filter(self.enfermedad_id == enfermedad_id).all()

