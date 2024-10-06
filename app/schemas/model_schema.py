from pydantic import BaseModel


class ModelBase(BaseModel):
    id: int
    name: str


class Model(ModelBase):
    pass
