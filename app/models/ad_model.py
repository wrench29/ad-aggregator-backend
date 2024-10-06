from sqlalchemy import Float, Column, Integer, String

from app.database import Base


class AdModel(Base):
    __tablename__ = "ads"

    platform = Column(String, primary_key=True)
    category = Column(String, primary_key=True)
    brand = Column(String, primary_key=True)
    model = Column(String, primary_key=True)
    price = Column(Float)
    region = Column(String)
    mileage = Column(Integer)
    color = Column(String)
