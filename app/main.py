from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from app import database
from app.services.ad_service import AdService

from .routers import ads


app = FastAPI()
app.include_router(ads.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
