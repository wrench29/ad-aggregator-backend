from fastapi import FastAPI
from dotenv import load_dotenv

from .routers import ads, info

load_dotenv()

app = FastAPI()
app.include_router(ads.router)
app.include_router(info.router)
