import os
from typing import Final

from fastapi import Depends
from sqlalchemy.orm import Session
import requests

from app.dependencies import get_db
from app.models.autoria_ads_count_statistics_model import AutoriaAdsCountStatisticsModel
from app.models.ad_model import AdModel
from app.models.autoria_brand_model import AutoriaBrandModel
from app.models.autoria_category_model import AutoriaCategoryModel
from app.models.autoria_model_model import AutoriaModelModel
from app.models.autoria_price_statistics_model import AutoriaPriceStatisticsModel
from app.repositories.cache_info_repo import CacheInfoRepository, get_cache_info_repository
from app.utils import AdsPeriod


class AutoriaRepository:
    __BASE_URL: Final = 'https://developers.ria.com/'

    def __init__(self, db: Session, cache_info_repository: CacheInfoRepository):
        self.db = db
        self.cache_info_repo = cache_info_repository
        self.__token = os.getenv('AUTORIA_TOKEN')

    def get_ad(self, id: int) -> AdModel:
        cache_key = f'ad_autoria_{id}'
        is_outdated = self.cache_info_repo.is_cache_outdated(cache_key)
        if not is_outdated:
            ad = self.db.query(AdModel).filter(
                AdModel.id == id, AdModel.platform == 'autoria').first()
            return ad
        self.db.query(AdModel).filter(
            AdModel.id == id, AdModel.platform == 'autoria').delete()
        url = f'{self.__BASE_URL}auto/info?auto_id={id}&api_key={self.__token}'
        json = AutoriaRepository.__make_request(url)
        self.get_categories()
        category_name = self.db.query(AutoriaCategoryModel).filter(
            AutoriaCategoryModel.id == json["autoData"]["categoryId"]).first().name
        ad_model = AdModel(
            id=id,
            platform='autoria',
            category=category_name,
            price=json["UAH"],
            model=json["modelName"],
            brand=json["markName"],
            region=json["stateData"]["regionName"],
            mileage=json["autoData"]["raceInt"],
            color=json["color"]["name"]
        )
        self.db.add(ad_model)
        self.db.commit()
        self.db.refresh(ad_model)
        self.cache_info_repo.update_cache_record(cache_key)
        return ad_model

    def get_categories(self) -> list[AutoriaCategoryModel]:
        cache_key = 'autoria_categories'
        is_outdated = self.cache_info_repo.is_cache_outdated(cache_key)
        if not is_outdated:
            categories = self.db.query(AutoriaCategoryModel).all()
            return categories
        self.db.query(AutoriaCategoryModel).delete()
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
        self.cache_info_repo.update_cache_record(cache_key)
        return categories

    def get_brands(self, category_id: int) -> list[AutoriaBrandModel]:
        cache_key = f'autoria_brands_{category_id}'
        is_outdated = self.cache_info_repo.is_cache_outdated(cache_key)
        if not is_outdated:
            brands = self.db.query(AutoriaBrandModel).filter(
                AutoriaBrandModel.category_id == category_id).all()
            return brands
        self.db.query(AutoriaBrandModel).filter(
            AutoriaBrandModel.category_id == category_id).delete()
        url = (
            f'{self.__BASE_URL}auto/categories/{category_id}/marks?'
            f'api_key={self.__token}'
        )
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
        self.cache_info_repo.update_cache_record(cache_key)
        return brands

    def get_models(self, category_id: int, brand_id: int) -> list[AutoriaModelModel]:
        cache_key = f'autoria_models_{category_id}_{brand_id}'
        is_outdated = self.cache_info_repo.is_cache_outdated(cache_key)
        if not is_outdated:
            models = self.db.query(AutoriaModelModel).filter(
                AutoriaModelModel.category_id == category_id,
                AutoriaModelModel.brand_id == brand_id).all()
            return models
        self.db.query(AutoriaModelModel).filter(
            AutoriaModelModel.category_id == category_id).delete()
        url = (
            f'{self.__BASE_URL}auto/categories/{category_id}'
            f'/marks/{brand_id}/models?api_key={self.__token}'
        )
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
        self.cache_info_repo.update_cache_record(cache_key)
        return models

    def get_ads_count_statistics(self,
                                 category_id: int,
                                 brand_id: int,
                                 model_id: int,
                                 period: AdsPeriod) -> AutoriaAdsCountStatisticsModel:
        top = 2 if period == AdsPeriod.DAY else 4 if period == AdsPeriod.WEEK else 5
        cache_key = (
            f'autoria_ads_count_statistics_{category_id}'
            f'_{brand_id}_{model_id}_{top}'
        )
        is_outdated = self.cache_info_repo.is_cache_outdated(cache_key)
        if not is_outdated:
            model = self.db.query(AutoriaAdsCountStatisticsModel).filter(
                AutoriaAdsCountStatisticsModel.category_id == category_id,
                AutoriaAdsCountStatisticsModel.brand_id == brand_id,
                AutoriaAdsCountStatisticsModel.model_id == model_id,
                AutoriaAdsCountStatisticsModel.period == top
            ).first()
            return model
        self.db.query(AutoriaAdsCountStatisticsModel).filter(
            AutoriaAdsCountStatisticsModel.category_id == category_id,
            AutoriaAdsCountStatisticsModel.brand_id == brand_id,
            AutoriaAdsCountStatisticsModel.model_id == model_id,
            AutoriaAdsCountStatisticsModel.period == top
        ).delete()
        url = (
            f'{self.__BASE_URL}auto/search?order_by=2&category_id={category_id}&'
            f'marka_id[0]={brand_id}&model_id[0]={model_id}&'
            f'top={top}&api_key={self.__token}'
        )
        json = AutoriaRepository.__make_request(url)
        ads_count = json["result"]["search_result"]["count"]
        statistics = AutoriaAdsCountStatisticsModel(
            category_id=category_id,
            brand_id=brand_id,
            model_id=model_id,
            period=top,
            ads_count=ads_count
        )
        self.db.add(statistics)
        self.db.commit()
        self.db.refresh(statistics)
        self.cache_info_repo.update_cache_record(cache_key)
        return statistics

    def get_price_statistics(self,
                             category_id: int,
                             brand_id: int,
                             model_id: int) -> AutoriaPriceStatisticsModel:
        cache_key = (
            f'autoria_price_statistics_{category_id}'
            f'_{brand_id}_{model_id}'
        )
        is_outdated = self.cache_info_repo.is_cache_outdated(cache_key)
        if not is_outdated:
            model = self.db.query(AutoriaPriceStatisticsModel).filter(
                AutoriaPriceStatisticsModel.category_id == category_id,
                AutoriaPriceStatisticsModel.brand_id == brand_id,
                AutoriaPriceStatisticsModel.model_id == model_id
            ).first()
            return model
        self.db.query(AutoriaPriceStatisticsModel).filter(
            AutoriaPriceStatisticsModel.category_id == category_id,
            AutoriaPriceStatisticsModel.brand_id == brand_id,
            AutoriaPriceStatisticsModel.model_id == model_id
        ).delete()
        url_get_cheapest = (
            f'{self.__BASE_URL}auto/search?order_by=2&'
            f'category_id={category_id}&marka_id[0]={brand_id}'
            f'&model_id[0]={model_id}&api_key={self.__token}'
        )
        url_get_expensive = (
            f'{self.__BASE_URL}auto/search?order_by=3&'
            f'category_id={category_id}&marka_id[0]={brand_id}'
            f'&model_id[0]={model_id}&api_key={self.__token}'
        )
        json_cheapest = AutoriaRepository.__make_request(url_get_cheapest)
        json_expensive = AutoriaRepository.__make_request(url_get_expensive)
        ads_cheapest = json_cheapest["result"]["search_result"]["ids"]
        ads_expensive = json_expensive["result"]["search_result"]["ids"]
        if len(ads_cheapest) == 0:
            self.db.commit()
            return None
        min_price_ad_id = ads_cheapest[0]
        max_price_ad_id = ads_expensive[0]
        min_price_ad = self.get_ad(min_price_ad_id)
        max_price_ad = self.get_ad(max_price_ad_id)

        statistics = AutoriaPriceStatisticsModel(
            category_id=category_id,
            brand_id=brand_id,
            model_id=model_id,
            min_price=min_price_ad.price,
            max_price=max_price_ad.price
        )

        self.db.add(statistics)
        self.db.commit()
        self.db.refresh(statistics)
        self.cache_info_repo.update_cache_record(cache_key)
        return statistics

    def __make_request(url: str) -> dict:
        return requests.get(url).json()


def get_autoria_repository(db: Session = Depends(get_db),
                           cache_info_repository: CacheInfoRepository = Depends(
                               get_cache_info_repository)
                           ) -> AutoriaRepository:
    return AutoriaRepository(db, cache_info_repository)
