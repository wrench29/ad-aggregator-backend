from sqlalchemy import Column, String

from app.database import Base


class UserModel(Base):
    __tablename__ = "user"

    username = Column(String, primary_key=True)
    password_hash = Column(String)
