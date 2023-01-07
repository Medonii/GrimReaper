from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    nickname: Union[str, None] = None
    password: Union[str, None] = None
    role: Union[str, None] = None
    ambulance: Union [str, None] = None

    