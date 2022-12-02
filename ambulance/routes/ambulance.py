from fastapi import APIRouter, HTTPException, status
from models.ambulance import ambulances
from config.db import conn
from schemas.ambulance import Ambulance



ambulance = APIRouter()

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
        tag = ambulance.tag
    ))
    return  conn.execute(ambulances.select()).fetchall()

@ambulance.put('/{id}')
async def update_ambulance(id: int, ambulance: Ambulance):
    conn.execute(ambulances.update().values(
        tag = ambulance.tag,
    ).where(ambulances.c.id == id))
    return  conn.execute(ambulances.select()).fetchall()

@ambulance.delete('/{id}')
async def delete_ambulance(id: int):
    conn.execute(ambulances.delete().where(ambulances.c.id == id))
    return  conn.execute(ambulances.select()).fetchall()