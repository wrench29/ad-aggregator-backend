from sqlalchemy import Column, String, DateTime

from app.database import Base


class CacheInfoModel(Base):
    __tablename__ = "cache_info"

    data_type = Column(String, primary_key=True)
    last_write = Column(DateTime)
