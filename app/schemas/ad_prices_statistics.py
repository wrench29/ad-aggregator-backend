from pydantic import BaseModel


class AdsPricesStatisticsBase(BaseModel):
    min_price: float
    max_price: float


class AdsPricesStatistics(AdsPricesStatisticsBase):
    pass
