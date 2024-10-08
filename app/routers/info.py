from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app import auth
from app.schemas.ad_prices_statistics import AdsPricesStatistics
from app.schemas.ads_count_statistics_schema import AdsCountStatistics
from app.schemas.brand_schema import Brand
from app.schemas.category_schema import Category
from app.schemas.model_schema import Model
from app.schemas.user_schema import User
from app.services.info_service import InfoService, get_info_service
from app.utils import AdsPeriod, Provider


router = APIRouter(prefix="/info",
                   tags=["Info"],
                   responses={
                       401: {'name': 'Unauthorized'}
                   })


@router.get("/providers")
async def get_available_providers(current_user: Annotated[User, Depends(auth.get_current_user)]):
    return ['autoria']


@router.get("/{provider}/categories", response_model=list[Category])
async def get_categories_from_provider(
    current_user: Annotated[User, Depends(auth.get_current_user)],
    provider: str = Path(description='Info provider', example='autoria'),
    service: InfoService = Depends(get_info_service)
):
    match provider:
        case 'autoria':
            return service.get_categories(Provider.AUTORIA)
        case _:
            return HTTPException(404, detail='Provider does not exist')


@router.get("/{provider}/{category_id}/brands", response_model=list[Brand])
async def get_brands_from_provider(
    current_user: Annotated[User, Depends(auth.get_current_user)],
    provider: str = Path(description='Info provider', example='autoria'),
    category_id: int = Path(),
    service: InfoService = Depends(get_info_service)
):
    match provider:
        case 'autoria':
            return service.get_brands(Provider.AUTORIA, category_id)
        case _:
            return HTTPException(404, detail='Provider does not exist')


@router.get("/{provider}/{category_id}/{brand_id}/models", response_model=list[Model])
async def get_models_from_provider(
    current_user: Annotated[User, Depends(auth.get_current_user)],
    provider: str = Path(description='Info provider', example='autoria'),
    category_id: int = Path(),
    brand_id: int = Path(),
    service: InfoService = Depends(get_info_service)
):
    match provider:
        case 'autoria':
            return service.get_models(Provider.AUTORIA, category_id, brand_id)
        case _:
            return HTTPException(404, detail='Provider does not exist')


@router.get("/{provider}/{category_id}/{brand_id}/{model_id}/prices", response_model=AdsPricesStatistics)
async def get_price_statistics_about_car(current_user: Annotated[User, Depends(auth.get_current_user)],
                                         provider: str = Path(
                                             description='Info provider', example='autoria'
),
        category_id: int = Path(),
        brand_id: int = Path(),
        model_id: int = Path(),
        service: InfoService = Depends(get_info_service)):
    match provider:
        case 'autoria':
            statistics = service.get_price_statistics(
                Provider.AUTORIA,
                category_id,
                brand_id,
                model_id
            )
            if statistics == None:
                return HTTPException(404, detail='No ads were found')
            return statistics
        case _:
            return HTTPException(404, detail='Provider does not exist')


@router.get("/{provider}/{category_id}/{brand_id}/{model_id}/ads_count", response_model=AdsCountStatistics)
async def get_ads_statistics_about_car(current_user: Annotated[User, Depends(auth.get_current_user)],
                                       provider: str = Path(
                                           description='Info provider', example='autoria'),
                                       category_id: int = Path(),
                                       brand_id: int = Path(),
                                       model_id: int = Path(),
                                       period: int = Query(
                                           description="Today = 1, Week = 2, Month = 3"),
                                       service: InfoService = Depends(
                                           get_info_service)
                                       ):
    if period < 1 or period > 3:
        return HTTPException(400, 'Period can only be 1, 2 or 3.')
    period_enum = AdsPeriod.DAY if period == 1 else AdsPeriod.WEEK if period == 2 else AdsPeriod.MONTH
    match provider:
        case 'autoria':
            return service.get_ad_statistics(
                Provider.AUTORIA,
                category_id,
                brand_id,
                model_id,
                period_enum
            )
        case _:
            return HTTPException(404, detail='Provider does not exist')
