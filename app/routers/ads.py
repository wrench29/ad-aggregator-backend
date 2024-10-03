from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Path, Query

router = APIRouter(prefix="/ads", tags=["Ads"])


@router.get("/saved")
async def get_saved_ads(start_date: Optional[datetime] = Query(None, description="Start date in ISO 8601 format", example="2000-10-01"),
                        end_date: Optional[datetime] = Query(None, description="End date in ISO 8601 format", example="2010-01-10")):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date."
        )
    return f"start_date: {start_date}, end_date: {end_date}"


@router.get("/statistics/{brand}/{model}")
async def get_statistics_about_car(brand: str = Path(description="Car brand", example="Toyota"),
                                   model: str = Path(description="Car model", example="Yaris")):
    return f"brand: {brand} model: {model}"


@router.get("")
async def get_ad_by_link(link: str = Query(description="URL to the ad", example="https://auto.ria.com/uk/auto_jaguar_f_pace_12344321.html")):
    return f"link to ad: {link}"
