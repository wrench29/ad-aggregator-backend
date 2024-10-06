from sqlalchemy import Column, String, Integer

from app.database import Base


class AutoriaModelModel(Base):
    __tablename__ = "autoria_model"

    id = Column(Integer, primary_key=True)
    name = Column(String)
