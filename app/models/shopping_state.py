from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db import db


class ShoppingState(db.Model):
    __tablename__ = "compra_estados"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    compras = relationship("Shopping", back_populates="estado")

    def __repr__(self):
        return (
            self.estado
        )

    @classmethod
    def get_all_estados(self):
        return ShoppingState.query.all()
        
    @staticmethod
    def get_by_id(id):
        return ShoppingState.query.get(id)