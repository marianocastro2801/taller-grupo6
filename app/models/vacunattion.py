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

        

    def __init__(self, fecha_vacunacion, paciente_id, enfermedad_id
    ):
        self.fecha_vacunacion= fecha_vacunacion
        self.paciente_id=paciente_id
        self.enfermedad_id = enfermedad_id

    def __repr__(self):
        return (
            self.fecha_vacunacion,

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

