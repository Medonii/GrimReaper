from pydantic import BaseModel

class Ambulance(BaseModel):
    tag: str
    position: str