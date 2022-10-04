from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, text, Date 
from sqlalchemy.dialects.mysql import TINYTEXT
from sqlalchemy.orm import relationship
from app.db import db


class Shopping(db.Model):
    __tablename__ = "compras_vacunas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=False, nullable=False)


    fecha_compra = Column(Date, unique=False, nullable=False)
    
    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    vacuna = relationship("Vaccine")

    cantidad_vacunas = Column(Integer, unique=False, nullable=False)

    lote_id = Column(Integer, ForeignKey("vacuna_lotes.id"), nullable=False)
    lote = relationship("VaccineLote")

    desarrollador_id = Column(Integer, ForeignKey("vacuna_desarrollador.id"), nullable=False)
    desarrollador = relationship("VaccineDeveloper")

    stock_id = Column(Integer, ForeignKey("vacuna_stock.id"), nullable=False)

    def __init__(self, nombre, vacuna_id, cantidad_vacunas, lote_id, desarrollador_id
    ):
        self.nombre = nombre,
        self.fecha_compra = datetime.today(),
        self.vacuna_id = vacuna_id
        self.cantidad_vacunas= cantidad_vacunas
        self.lote_id = lote_id
        self.desarrollador_id = desarrollador_id
        self.stock_id= None 

    def __repr__(self):
        return "<Shopping(nombre='%s', )>" % (
            self.nombre,
        )

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

#arreglar para stock
    @classmethod
    def get_cant_stock(shopping):
        total = shopping.cantidad_vacunas.split()
        return sum(total)