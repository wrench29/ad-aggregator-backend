from sqlalchemy import Column, String, Integer

from app.database import Base


class AutoriaBrandModel(Base):
    __tablename__ = "autoria_brand"

    id = Column(Integer, primary_key=True)
    name = Column(String)
