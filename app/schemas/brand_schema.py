from pydantic import BaseModel


class BrandBase(BaseModel):
    id: int
    name: str


class Brand(BrandBase):
    pass
