from venv import logger
from fastapi import APIRouter, HTTPException, status, Depends
from models.ambulance import ambulances
from config.db import conn
from schemas.ambulance import Ambulance
from typing import List
from user.auth.user_auth import get_user
from user.schemas.user import User

ambulance = APIRouter()

class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")

@ambulance.get('/')
async def fetch_ambulances():
    return conn.execute(ambulances.select()).fetchall()

@ambulance.get('/{id}')
async def fetch_ambulance(id: int):
    return conn.execute(ambulances.select().where(ambulances.c.id == id)).first()

@ambulance.post('/')
async def create_ambulance(ambulance: Ambulance):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.tag == ambulance.tag)).first()
    if ambulance_db is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this tag already exist"
        )
    conn.execute(ambulances.insert().values(
        tag = ambulance.tag,
        type = ambulance.type,
        status = 'Free',
        position = ambulance.position
    ))
    return  "Ambulance created"

@ambulance.put('/update/{id}')
async def update_ambulance(id: int, ambulance: Ambulance):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.update().values(
        tag = ambulance.tag,
        type = ambulance.type,
        position = ambulance.position
    ).where(ambulances.c.id == id))
    return  "Ambulance updated"

@ambulance.put('/set_busy_status/{id}')
async def set_ambulance_as_busy(id: int):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.update().values(
        status = 'Busy'
    ).where(ambulances.c.id == id))
    return  "Ambulance set as busy"

@ambulance.put('/make_available/{id}')
async def make_available(id: int):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.update().values(
        status = 'Free'
    ).where(ambulances.c.id == id))
    return  "Ambulanced made available"

@ambulance.put('/exclude/{id}')
async def exclude_ambulance(id: int):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.update().values(
        status = 'Not Available'
    ).where(ambulances.c.id == id))
    return  "Ambulance excluded"

@ambulance.delete('/{id}')
async def delete_ambulance(id: int):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.delete().where(ambulances.c.id == id))
    return  "Ambulance deleted"
