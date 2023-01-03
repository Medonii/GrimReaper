from pydantic import BaseModel
from typing import Union
from enum import Enum

class User(BaseModel):
    id: int
    nickname: str
    password: str

class UserBody(BaseModel):
    nickname: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Ambulance(BaseModel):
    tag: str
    type: str
    status: str
    position: str

class AmbulanceBody(BaseModel):
    tag: str
    type: str
    position: str

class Statuses(Enum):
    A = 'Ambulance Assigned'
    R = 'Registered'
    X = 'Rejected'
    F = 'Finished'
    P = 'In Progress'

class Patient(BaseModel):
    name: Union[str, None]
    address: Union[str, None]
    ambulance: Union[str, None] = None
    status: Union[Statuses, None] = None
    people: Union[int, None] = 1
    type: Union[str, None]