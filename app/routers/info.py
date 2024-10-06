from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.services.info_service import InfoService, Provider, get_info_service


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


@router.get("/{provider}/models")
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


@router.get("/prices/{provider}/{category}/{brand}/{model}")
async def get_price_statistics_about_car(provider: str = Path(),
                                         category_id: int = Path(),
                                         brand_id: int = Path(),
                                         model_id: int = Path()):
    return f"category: {category_id} brand: {brand_id} model: {model_id}"


@router.get("/ads_count/{provider}/{category}/{brand}/{model}")
async def get_ads_statistics_about_car(provider: str = Path(),
                                       category_id: int = Path(),
                                       brand_id: int = Path(),
                                       model_id: int = Path(),
                                       period: int = Query(description="Today = 1, Week = 2, Month = 3")):
    return f"category: {category_id} brand: {brand_id} model: {model_id}"
