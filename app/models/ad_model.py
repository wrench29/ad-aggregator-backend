from sqlalchemy import Float, Column, Integer, String

from app.database import Base


class AdModel(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    platform = Column(String, primary_key=True)
    category = Column(String)
    brand = Column(String)
    model = Column(String)
    price = Column(Float)
    region = Column(String)
    mileage = Column(Integer)
    color = Column(String)
