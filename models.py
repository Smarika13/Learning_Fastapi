from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    in_stock = Column(Boolean)