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
    ambulance: Union[str, None] = None
    status: Union[Statuses, None] = None