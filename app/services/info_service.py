from enum import Enum

from fastapi import Depends

from app.repositories.autoria_repo import AdPeriod, AutoriaRepository, get_autoria_repository
from app.schemas.brand_schema import Brand
from app.schemas.category_schema import Category
from app.schemas.model_schema import Model


class Provider(Enum):
    AUTORIA = 1


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
                brand_models = self.autoria_repo.get_brands()
                brands = []
                for brand in brand_models:
                    brands.append(
                        Brand(id=brand.id, name=brand.name)
                    )
                return brands

    def get_models(self, provider: Provider, category_id: int, brand_id: int) -> list[Model]:
        match provider:
            case Provider.AUTORIA:
                model_models = self.autoria_repo.get_models()
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
                             model_id: int):
        pass

    def get_ad_statistics(self,
                          provider: Provider,
                          category_id: int,
                          brand_id: int,
                          model_id: int,
                          period: AdPeriod):
        pass


def get_info_service(
        autoria_repository: AutoriaRepository = Depends(get_autoria_repository)) -> InfoService:
    return InfoService(autoria_repository)
