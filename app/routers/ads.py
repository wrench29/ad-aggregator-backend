from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.models.ad_model import AdModel
from app.services.ad_service import AdService, get_ad_service

router = APIRouter(prefix="/ads", tags=["Ads"])


@router.get("")
async def get_ad_by_link(link: str = Query(description="URL to the ad", example="https://auto.ria.com/uk/auto_jaguar_f_pace_12344321.html"),
                         service: AdService = Depends(get_ad_service)):
    return f"link to ad: {link}"


@router.get("/{provider}/{id}")
async def get_ad_from_provider_by_id(id: int, service: AdService = Depends(get_ad_service)):
    service.save_ad(None)
    return f"id of ad: {id}"
