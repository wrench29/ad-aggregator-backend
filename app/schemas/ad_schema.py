from pydantic import BaseModel


class AdBase(BaseModel):
    name: str
    price: float
    model: str
    brand: str
    region: str
    mileage: int
    color: str
    interior: str
    contacts: str


class AdCreate(AdBase):
    pass


class Ad(AdBase):
    id: int

    class Config:
        orm_mode = True
