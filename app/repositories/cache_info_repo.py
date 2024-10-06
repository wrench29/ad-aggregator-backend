from datetime import datetime
from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.cache_info_model import CacheInfoModel


class CacheInfoRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def is_cache_outdated(self, data_type: str) -> bool:
        record = self.__get_cache_record(data_type)
        if record == None:
            return True
        diff = datetime.now() - record
        if diff.days > 0:
            return True
        return False

    def update_cache_record(self, data_type: str):
        model = self.db.query(CacheInfoModel).filter(
            CacheInfoModel.data_type == data_type).first()
        current_datetime = datetime.now()
        if model == None:
            model = CacheInfoModel(data_type=data_type,
                                   last_write=current_datetime)
            self.db.add(model)
        else:
            model.last_write = current_datetime
        self.db.commit()
        self.db.refresh(model)

    def __get_cache_record(self, data_type: str) -> Optional[datetime]:
        model = self.db.query(CacheInfoModel).filter(
            CacheInfoModel.data_type == data_type).first()
        if model == None:
            return None
        return model.last_write


def get_cache_info_repository(db: Session = Depends(get_db)) -> CacheInfoRepository:
    return CacheInfoRepository(db)
