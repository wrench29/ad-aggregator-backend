from sqlalchemy import Column, Integer

from app.database import Base


class AutoriaAdsCountStatisticsModel(Base):
    __tablename__ = "autoria_ads_count_statistics"

    category_id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, primary_key=True)
    ads_count = Column(Integer)
