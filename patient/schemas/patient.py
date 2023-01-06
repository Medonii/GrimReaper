from pydantic import BaseModel
from typing import Union, Optional
from enum import Enum

class Statuses(Enum):
    A = 'Ambulance Assigned'
    S = "Ambulance Suggested"
    R = 'Registered'
    X = 'Rejected'
    P = 'In Progress'
    F = 'Finished'


class Patient(BaseModel):
    name: Union[str, None]
    address: Union[str, None]
    ambulance: Union[str, None] = None
    status: Union[Statuses, None] = None
    people: Union[int, None] = 1
    type: Union[str, None]