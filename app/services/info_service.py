from enum import Enum

from fastapi import Depends

from app.repositories.autoria_repo import AutoriaRepository, get_autoria_repository
from app.schemas.ad_prices_statistics import AdsPricesStatistics
from app.schemas.ads_count_statistics_schema import AdsCountStatistics
from app.schemas.brand_schema import Brand
from app.schemas.category_schema import Category
from app.schemas.model_schema import Model
from app.utils import AdsPeriod, Provider


class InfoService():
    def __init__(self,
                 autoria_repository: AutoriaRepository):
        self.autoria_repo = autoria_repository

    def get_categories(self, provider: Provider) -> list[Category]:
        match provider:
            case Provider.AUTORIA:
                category_models = self.autoria_repo.get_categories()
                categories = []
                for category in category_models:
                    categories.append(
                        Category(id=category.id, name=category.name)
                    )
                return categories

    def get_brands(self, provider: Provider, category_id: int) -> list[Brand]:
        match provider:
            case Provider.AUTORIA:
                brand_models = self.autoria_repo.get_brands(category_id)
                brands = []
                for brand in brand_models:
                    brands.append(
                        Brand(id=brand.id, name=brand.name)
                    )
                return brands

    def get_models(self, provider: Provider, category_id: int, brand_id: int) -> list[Model]:
        match provider:
            case Provider.AUTORIA:
                model_models = self.autoria_repo.get_models(
                    category_id, brand_id
                )
                models = []
                for model in model_models:
                    models.append(
                        Model(id=model.id, name=model.name)
                    )
                return models

    def get_price_statistics(self,
                             provider: Provider,
                             category_id: int,
                             brand_id: int,
                             model_id: int) -> AdsPricesStatistics:
        match provider:
            case Provider.AUTORIA:
                price_statistics_model = self.autoria_repo.get_price_statistics(
                    category_id,
                    brand_id,
                    model_id
                )
                if price_statistics_model == None:
                    return None
                price_statistics = AdsPricesStatistics(
                    min_price=price_statistics_model.min_price,
                    max_price=price_statistics_model.max_price
                )
                return price_statistics

    def get_ad_statistics(self,
                          provider: Provider,
                          category_id: int,
                          brand_id: int,
                          model_id: int,
                          period: AdsPeriod) -> AdsCountStatistics:
        match provider:
            case Provider.AUTORIA:
                ads_count_statistics_model = self.autoria_repo.get_ads_count_statistics(
                    category_id,
                    brand_id,
                    model_id,
                    period
                )
                ads_count_statistics = AdsCountStatistics(
                    count=ads_count_statistics_model.ads_count
                )
                return ads_count_statistics


def get_info_service(
        autoria_repository: AutoriaRepository = Depends(get_autoria_repository)) -> InfoService:
    return InfoService(autoria_repository)
