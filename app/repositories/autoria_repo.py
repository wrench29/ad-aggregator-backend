from datetime import datetime
from enum import Enum
import os
from typing import Final, Optional

from fastapi import Depends
from sqlalchemy.orm import Session
import requests

from app.dependencies import get_db
from app.models.autoria_ads_count_statistics_model import AutoriaAdsCountStatisticsModel
from app.models import ad_model
from app.models.autoria_brand_model import AutoriaBrandModel
from app.models.autoria_category_model import AutoriaCategoryModel
from app.models.autoria_model_model import AutoriaModelModel
from app.models.autoria_price_statistics_model import AutoriaPriceStatisticsModel
from app.models.cache_info_model import CacheInfoModel
from app.repositories.cache_info_repo import CacheInfoRepository, get_cache_info_repository


class AdPeriod(Enum):
    DAY = 1
    WEEK = 2
    MONTH = 3


class AutoriaRepository:
    __BASE_URL: Final = 'https://developers.ria.com/'

    def __init__(self, db: Session, cache_info_repository: CacheInfoRepository):
        self.db = db
        self.cache_info_repo = cache_info_repository
        self.__token = os.getenv('AUTORIA_TOKEN')

    def get_ad(self, id: int) -> ad_model.AdModel:
        pass

    def get_categories(self) -> list[AutoriaCategoryModel]:
        is_outdated = self.cache_info_repo.is_cache_outdated(
            'autoria_categories')
        if not is_outdated:
            categories = self.db.query(AutoriaCategoryModel).all()
            return categories
        AutoriaCategoryModel.query().delete()
        url = f'{self.__BASE_URL}auto/categories?api_key={self.__token}'
        json = AutoriaRepository.__make_request(url)
        categories = []
        for entry in json:
            categories.append(
                AutoriaCategoryModel(
                    id=entry['value'],
                    name=entry['name']
                )
            )
        self.db.add_all(categories)
        self.db.commit()
        for category in categories:
            self.db.refresh(category)
        self.cache_info_repo.update_cache_record('autoria_categories')
        return categories

    def get_brands(self, category_id: int) -> list[AutoriaBrandModel]:
        is_outdated = self.cache_info_repo.is_cache_outdated(
            f'autoria_brands_{category_id}')
        if not is_outdated:
            brands = self.db.query(AutoriaBrandModel).filter(
                AutoriaBrandModel.category_id == category_id).all()
            return brands
        self.db.query(AutoriaBrandModel).filter(
            AutoriaBrandModel.category_id == category_id).delete()
        url = f'{
            self.__BASE_URL}auto/categories/{category_id}/marks?api_key={self.__token}'
        json = AutoriaRepository.__make_request(url)
        brands = []
        for entry in json:
            brands.append(
                AutoriaBrandModel(
                    id=entry['value'],
                    category_id=category_id,
                    name=entry['name']
                )
            )
        self.db.add_all(brands)
        self.db.commit()
        for brand in brands:
            self.db.refresh(brand)
        self.cache_info_repo.update_cache_record(
            f'autoria_brands_{category_id}')
        return brands

    def get_models(self, category_id: int, brand_id: int) -> list[AutoriaModelModel]:
        is_outdated = self.cache_info_repo.is_cache_outdated(
            f'autoria_models_{category_id}_{brand_id}')
        if not is_outdated:
            models = self.db.query(AutoriaModelModel).filter(
                AutoriaModelModel.category_id == category_id).all()
            return models
        self.db.query(AutoriaModelModel).filter(
            AutoriaModelModel.category_id == category_id).delete()
        url = f'{self.__BASE_URL}auto/categories/{category_id}'
        + f'/marks/{brand_id}/models?api_key={self.__token}'
        json = AutoriaRepository.__make_request(url)
        models = []
        for entry in json:
            models.append(
                AutoriaModelModel(
                    id=entry['value'],
                    category_id=category_id,
                    brand_id=brand_id,
                    name=entry['name']
                )
            )
        self.db.add_all(models)
        self.db.commit()
        for model in models:
            self.db.refresh(model)
        self.cache_info_repo.update_cache_record(
            f'autoria_models_{category_id}_{brand_id}')
        return models

    def get_ads_count_statistics(self,
                                 category_id: int,
                                 brand_id: int,
                                 model_id: int,
                                 period: AdPeriod) -> AutoriaAdsCountStatisticsModel:
        pass

    def get_price_statictics(self,
                             category_id: int,
                             brand_id: int,
                             model_id: int) -> AutoriaPriceStatisticsModel:
        pass

    def __make_request(url: str) -> dict:
        return requests.get(url).json()


def get_autoria_repository(db: Session = Depends(get_db),
                           cache_info_repository: CacheInfoRepository = Depends(
                               get_cache_info_repository)
                           ) -> AutoriaRepository:
    return AutoriaRepository(db, cache_info_repository)
