from pydantic import BaseModel


class AdBase(BaseModel):
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
