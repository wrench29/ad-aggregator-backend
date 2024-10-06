from sqlalchemy import Column, String, Integer

from app.database import Base


class AutoriaModelModel(Base):
    __tablename__ = "autoria_model"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer)
    brand_id = Column(Integer)
    name = Column(String)
