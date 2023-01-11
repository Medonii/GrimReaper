from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from models.ambulance import ambulances
from config.db import conn
from schemas.ambulance import Ambulance
import requests

ambulance = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://user:80/token",
    scopes={"admin": "Do everything.", "operator": "Operate requests", "ambulance_driver": "Read requests, update ambulance."},
    )


@ambulance.get('/')
async def fetch_ambulances(token: str = Depends(oauth2_scheme)):

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                        "Content-Type": "application/json",
                        'Authorization': "Bearer " + token,
                    })

    if(response.json().get('nickname') is not None):
        return conn.execute(ambulances.select()).fetchall()
    else:
        return response.json()

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
