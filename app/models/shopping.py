from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, text, Date
from datetime import datetime
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class Shopping(db.Model):
    __tablename__ = "compras_vacunas"
    id = Column(Integer, primary_key=True)

    fecha_compra = Column(Date, unique=False, nullable=False)
    
    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    vacuna = relationship("Vaccine")

    cantidad_vacunas = Column(Integer, unique=False, nullable=False)

    lote_id = Column(Integer, ForeignKey("vacuna_lotes.id"), nullable=False)
    lote = relationship("VaccineLote")

    desarrollador_id = Column(Integer, ForeignKey("vacuna_desarrollador.id"), nullable=False)
    desarrollador = relationship("VaccineDeveloper")

    stock_id = Column(Integer, ForeignKey("vacuna_stock.id"), nullable=False)

    stock_nacional = Column(Integer, unique=False, nullable=False)

    enfermedad_id = Column(Integer, ForeignKey("vacuna_enfermedad.id"), nullable=False)
    enfermedad = relationship("VaccineEnfermedad")

    
    estado_id = Column(Integer, ForeignKey("compra_estados.id"), nullable=False)
    estado = relationship("ShoppingState")

#    cantidad_vencida = Column(Integer, unique=False, nullable=False)

    def __init__(self, vacuna_id, cantidad_vacunas, lote_id, desarrollador_id, enfermedad_id
    ):
        self.fecha_compra = datetime.today()
        self.vacuna_id = vacuna_id
        self.cantidad_vacunas= cantidad_vacunas
        self.lote_id = lote_id
        self.enfermedad_id = enfermedad_id
        self.desarrollador_id = desarrollador_id
        self.stock_id= None 
        self.stock_nacional = 0
        self.estado_id = 1
#        self.cantidad_vencida = 0
        

    def save(self):
        db.session.add(self)
        db.session.commit()
        

    @staticmethod
    def update():
        db.session.commit()


    @staticmethod
    def get_by_id(shopping_id):
        with db.session.no_autoflush:
            return Shopping.query.get(shopping_id)


    @staticmethod
    def get_all_shoppings():
        return Shopping.query.all()

    
    @staticmethod
    def all():
        return Shopping.query.all()

    @staticmethod
    def update(**kwargs):
            shopping = Shopping.get_by_id(kwargs["id"])
            for key, value in kwargs.items():
                setattr(shopping, key, value)
            db.session.commit()

    @classmethod
    def get_shoppings_by_vaccine(self, vaccine_id):
        return Shopping.query.filter(self.vacuna_id == vaccine_id).all()

    @classmethod
    def get_lotes_by_vaccine(self, vaccine_id):
        return Shopping.query.filter(self.vacuna_id == vaccine_id).all()


    @staticmethod
    def get_filtered(enfermedad_id):
   
        return Shopping.query.filter(Shopping.enfermedad_id == enfermedad_id) 


    def pagar(self):
        self.estado_id = "2"
        db.session.commit()

    def entregar(self):
        self.estado_id = "3"
        db.session.commit()

    