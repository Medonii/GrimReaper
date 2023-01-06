from pydantic import BaseModel
from typing import Union
from enum import Enum

class Roles(Enum):
    OP = 'Operator'
    AD = 'Admin'
    DR = 'Ambulance driver'

class User(BaseModel):
    nickname: Union[str, None] = None
    password: Union[str, None] = None
    role: Union[Roles, None] = None
    ambulance: Union[str, None] = None

class UserBody(BaseModel):
    nickname: Union[str, None] = None
    password: Union[str, None] = None


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