from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import ad_schema
from app.models import ad_model


class AdRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_ad(self, ad: ad_schema.Ad) -> ad_model.AdModel:
        ad_db = ad_model.AdModel(
            name=ad.name,
            price=ad.price,
            model=ad.model,
            brand=ad.brand,
            region=ad.region,
            mileage=ad.mileage,
            color=ad.color,
            interior=ad.interior,
            contacts=ad.contacts
        )
        self.db.add(ad_db)
        self.db.commit()
        self.db.refresh(ad_db)
        return ad_db


def get_ad_repository(db: Session = Depends(get_db)) -> AdRepository:
    return AdRepository(db)
