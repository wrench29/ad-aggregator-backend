from fastapi import Depends

from app.models import ad_model
from app.repositories.ad_repo import AdRepository, get_ad_repository
from app.schemas import ad_schema


class AdService():
    def __init__(self, ad_repository: AdRepository = Depends(get_ad_repository)):
        self.ad_repo = ad_repository

    def view_ad_by_link(self, link: str) -> ad_model.AdModel:
        pass

    def save_ad(self, ad: ad_schema.Ad) -> ad_model.AdModel:
        return self.ad_repo.create_ad(ad)


def get_ad_service(ad_repository: AdRepository = Depends(get_ad_repository)) -> AdService:
    return AdService(ad_repository)
