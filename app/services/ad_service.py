from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException, status

from app.models import ad_model
from app.repositories.ad_repo import AdRepository, get_ad_repository
from app.repositories.autoria_repo import AutoriaRepository, get_autoria_repository
from app.schemas import ad_schema
from app.utils import Provider, provider_to_str


class AdService():
    def __init__(self,
                 ad_repository: AdRepository,
                 autoria_repository: AutoriaRepository):
        self.ad_repo = ad_repository
        self.autoria_repo = autoria_repository

    def get_ad_by_link(self, link: str) -> ad_schema.Ad:
        exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail='Unknown ads provider')
        if 'ria.com' in link:
            html_file = link.split('/')[-1]
            name = html_file.split('.')[0]
            id = None
            try:
                id = int(name.split('_')[-1])
            except:
                raise exception
            if id <= 0:
                raise exception
            ad_model = self.autoria_repo.get_ad(id)
            return ad_schema.Ad(
                id=ad_model.id,
                platform=ad_model.platform,
                category=ad_model.category,
                brand=ad_model.brand,
                model=ad_model.model,
                price=ad_model.price,
                region=ad_model.region,
                mileage=ad_model.mileage,
                color=ad_model.color
            )
        else:
            raise exception

    def get_ad_by_id_and_provider(self, id: int, provider: Provider) -> ad_schema.Ad:
        match provider:
            case Provider.AUTORIA:
                ad_model_ = self.autoria_repo.get_ad(id)
                return ad_schema.Ad(
                    id=ad_model_.id,
                    platform=ad_model_.platform,
                    category=ad_model_.category,
                    brand=ad_model_.brand,
                    model=ad_model_.model,
                    price=ad_model_.price,
                    region=ad_model_.region,
                    mileage=ad_model_.mileage,
                    color=ad_model_.color
                )

    def save_ad(self, username: str, id: int, provider: Provider) -> ad_model.AdModel:
        ad = None
        match provider:
            case Provider.AUTORIA:
                ad = self.autoria_repo.get_ad(id)
        if ad == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Ad with specified ID does not exist'
            )
        self.ad_repo.save_ad(username, id, provider)
        return ad

    def get_saved_ads(self, username: str, from_: Optional[datetime], to_: Optional[datetime]) -> list[ad_schema.SavedAd]:
        saved_ads_models = self.ad_repo.get_saved_ads(username, from_, to_)
        saved_ads = []
        for saved_ad_model in saved_ads_models:
            saved_ads.append(
                ad_schema.SavedAd(
                    id=saved_ad_model.id,
                    save_time=saved_ad_model.save_time,
                    platform=saved_ad_model.ad.platform,
                    category=saved_ad_model.ad.category,
                    brand=saved_ad_model.ad.brand,
                    model=saved_ad_model.ad.model,
                    price=saved_ad_model.ad.price,
                    region=saved_ad_model.ad.region,
                    mileage=saved_ad_model.ad.mileage,
                    color=saved_ad_model.ad.color
                )
            )
        return saved_ads

    def delete_saved_ad(self, username: str, id: int, provider: Provider):
        self.ad_repo.delete_saved_ad(username, id, provider_to_str(provider))


def get_ad_service(
        ad_repository: AdRepository = Depends(get_ad_repository),
        autoria_repository: AutoriaRepository = Depends(get_autoria_repository)) -> AdService:
    return AdService(ad_repository, autoria_repository)
