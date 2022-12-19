from pydantic import BaseModel
from enum import Enum

class Statuses(Enum):
    P = 'P'
    N = 'N'
    V = 'V'
    T = 'T'
    S = 'S'

class Ambulance(BaseModel):
    tag: str
    type: str