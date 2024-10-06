from sqlalchemy import Column, Float, Integer

from app.database import Base


class AutoriaPriceStatisticsModel(Base):
    __tablename__ = "autoria_price_statistics"

    category_id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, primary_key=True)
    min_price = Column(Float)
    max_price = Column(Float)
