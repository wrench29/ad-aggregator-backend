from enum import Enum
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import ad_schema
from app.models import ad_model


class AdPeriod(Enum):
    DAY = 1
    WEEK = 2
    MONTH = 3


class AutoriaRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_ad(self, id: int) -> ad_model.AdModel:
        pass

    def get_categories(self) -> int:
        pass

    def get_brands(self, category: int) -> int:
        pass

    def get_models(self, brand: int) -> int:
        pass

    def get_statistics(self, model: int, period: AdPeriod) -> int:
        pass


def get_autoria_repository(db: Session = Depends(get_db)) -> AutoriaRepository:
    return AutoriaRepository(db)
