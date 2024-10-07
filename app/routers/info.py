from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.services.info_service import InfoService, Provider, get_info_service
from app.utils import AdsPeriod


router = APIRouter(prefix="/info", tags=["Info"])


@router.get("/providers")
async def get_available_providers():
    return ['autoria']


@router.get("/{provider}/categories")
async def get_categories_from_provider(
    provider: str = Path(description='Info provider', example='autoria'),
    service: InfoService = Depends(get_info_service)
):
    match provider:
        case 'autoria':
            return service.get_categories(Provider.AUTORIA)
        case _:
            return HTTPException(404, detail='Provider does not exist')


@router.get("/{provider}/{category_id}/brands")
async def get_brands_from_provider(
    provider: str = Path(description='Info provider', example='autoria'),
    category_id: int = Path(),
    service: InfoService = Depends(get_info_service)
):
    match provider:
        case 'autoria':
            return service.get_brands(Provider.AUTORIA, category_id)
        case _:
            return HTTPException(404, detail='Provider does not exist')


@router.get("/{provider}/{category_id}/{brand_id}/models")
async def get_models_from_provider(
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


@router.get("/prices/{provider}/{category_id}/{brand_id}/{model_id}")
async def get_price_statistics_about_car(provider: str = Path(),
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


@router.get("/ads_count/{provider}/{category_id}/{brand_id}/{model_id}")
async def get_ads_statistics_about_car(provider: str = Path(),
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
