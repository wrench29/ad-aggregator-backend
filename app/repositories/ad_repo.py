from datetime import datetime
from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.ad_model import AdModel
from app.models.saved_ad_model import SavedAdModel
from app.schemas import ad_schema
from app.utils import provider_to_str


class AdRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_ad(self, username: str, id: int, provider: str) -> SavedAdModel:
        saved_ad = SavedAdModel(
            username=username,
            provider=provider_to_str(provider),
            id=id,
            save_time=datetime.now(),
        )
        self.db.add(saved_ad)
        self.db.commit()
        self.db.refresh(saved_ad)
        return saved_ad

    def get_saved_ads(self,
                      username: str,
                      from_: Optional[datetime],
                      to_: Optional[datetime]) -> list[SavedAdModel]:
        query = self.db.query(SavedAdModel).filter(
            SavedAdModel.username == username
        )
        if from_ != None:
            query = query.filter(SavedAdModel.save_time >= from_)
        if to_ != None:
            query = query.filter(SavedAdModel.save_time <= to_)
        return query.all()

    def delete_saved_ad(self, username: str, id: int, provider: str):
        self.db.query(SavedAdModel).filter(
            SavedAdModel.username == username,
            SavedAdModel.id == id,
            SavedAdModel.provider == provider
        ).delete()
        self.db.commit()


def get_ad_repository(db: Session = Depends(get_db)) -> AdRepository:
    return AdRepository(db)
