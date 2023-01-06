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
    