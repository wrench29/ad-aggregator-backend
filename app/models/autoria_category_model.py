from sqlalchemy import Column, String, Integer

from app.database import Base


class AutoriaCategoryModel(Base):
    __tablename__ = "autoria_category"

    id = Column(Integer, primary_key=True)
    name = Column(String)
