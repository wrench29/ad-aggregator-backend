from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app import auth
from app.schemas.ad_schema import Ad, AdToSave, SavedAd
from app.schemas.user_schema import User
from app.services.ad_service import AdService, get_ad_service
from app.utils import Provider, provider_from_str

router = APIRouter(prefix="/ads",
                   tags=["Ads"],
                   responses={
                       401: {'name': 'Unauthorized'}
                   })


def verify_provider(provider_str: str) -> Provider:
    provider_enum = provider_from_str(provider_str)
    if provider_enum == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Unknown provider')
    return provider_enum


@router.get("", response_model=Ad)
async def get_ad_by_link(current_user: Annotated[User, Depends(auth.get_current_user)],
                         link: str = Query(
                             description="URL to the ad", example="https://auto.ria.com/uk/auto_jaguar_f_pace_12344321.html"),
                         service: AdService = Depends(get_ad_service)):
    return service.get_ad_by_link(link)


@router.get("/{provider}/{id}", response_model=Ad)
async def get_ad_from_provider_by_id(current_user: Annotated[User, Depends(auth.get_current_user)],
                                     provider: str = Path(
                                         description='Info provider', example='autoria'),
                                     id: int = Path(),
                                     service: AdService = Depends(get_ad_service)):
    service.get_ad_by_id_and_provider(id, verify_provider(provider))


@router.post("")
async def save_ad(current_user: Annotated[User, Depends(auth.get_current_user)],
                  ad_to_save: AdToSave,
                  service: AdService = Depends(get_ad_service)):
    service.save_ad(current_user.username, ad_to_save.id, verify_provider(
        ad_to_save.provider))


@router.get("/saved", response_model=list[SavedAd])
async def get_saved_ads(current_user: Annotated[User, Depends(auth.get_current_user)],
                        start_date: Optional[datetime] = Query(
                            None, description="Start date in ISO 8601 format", example="2000-10-01"),
                        end_date: Optional[datetime] = Query(
                            None, description="End date in ISO 8601 format", example="2010-01-10"),
                        service: AdService = Depends(get_ad_service)):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date."
        )
    return service.get_saved_ads(current_user.username, start_date, end_date)


@router.delete("/saved/{provider}/{id}")
async def remove_saved_ad(current_user: Annotated[User, Depends(auth.get_current_user)],
                          provider: str = Path(
                              description='Info provider', example='autoria'),
                          id: int = Path(),
                          service: AdService = Depends(get_ad_service)):
    service.delete_saved_ad(current_user.username, id,
                            verify_provider(provider))
