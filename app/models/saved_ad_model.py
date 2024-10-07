from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class SavedAdModel(Base):
    __tablename__ = "saved_ad"

    username = Column(String, ForeignKey("user.username"), primary_key=True)
    provider = Column(String, ForeignKey("ads.platform"), primary_key=True)
    id = Column(Integer, ForeignKey("ads.id"), primary_key=True)
    save_time = Column(DateTime)

    ad = relationship(
        "AdModel",
        foreign_keys=[provider, id],
        primaryjoin="and_(SavedAdModel.provider == AdModel.platform, SavedAdModel.id == AdModel.id)",
        backref="saved_ads"
    )
