from datetime import datetime
from pydantic import BaseModel


class AdBase(BaseModel):
    id: int
    platform: str
    category: str
    brand: str
    model: str
    price: float
    region: str
    mileage: int
    color: str


class AdCreate(AdBase):
    pass


class Ad(AdBase):
    class Config:
        orm_mode = True


class AdToSave(BaseModel):
    id: int
    provider: str


class SavedAd(AdBase):
    save_time: datetime
