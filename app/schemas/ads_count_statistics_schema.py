from pydantic import BaseModel


class AdsCountStatisticsBase(BaseModel):
    count: int


class AdsCountStatistics(AdsCountStatisticsBase):
    pass
