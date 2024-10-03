from fastapi import FastAPI

from .routers import ads

app = FastAPI()
app.include_router(ads.router)
