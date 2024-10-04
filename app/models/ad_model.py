from sqlalchemy import Float, Column, Integer, String

from app.database import Base


class AdModel(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    model = Column(String)
    brand = Column(String)
    region = Column(String)
    mileage = Column(Integer)
    color = Column(String)
    interior = Column(String)
    contacts = Column(String)
