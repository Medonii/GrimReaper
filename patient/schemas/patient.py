from pydantic import BaseModel
from typing import Union, Optional
from enum import Enum

class Statuses(Enum):
    A = 'Ambulance Assigned'
    R = 'Registered'
    X = 'Rejected'


class Patient(BaseModel):
    name: Union[str, None]
    address: Union[str, None]
    ambulance: Union[str, None]
    status: Union[Statuses, None] = None
    people: Union[int, None] = 1
    type: Union[str, None]