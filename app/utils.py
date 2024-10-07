from enum import Enum
from typing import Optional


class AdsPeriod(Enum):
    DAY = 1
    WEEK = 2
    MONTH = 3


class Provider(Enum):
    AUTORIA = 1


def provider_from_str(provider_str: str) -> Optional[Provider]:
    match provider_str.lower():
        case 'autoria':
            return Provider.AUTORIA
    return None


def provider_to_str(provider: Provider) -> str:
    match provider:
        case Provider.AUTORIA:
            return 'autoria'
