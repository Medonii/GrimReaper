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
async def fetch_ambulance(id: int, token: str = Depends(oauth2_scheme)):

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    if(response.json().get('nickname') is not None):
       return conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    else:
       return response.json()
        

@ambulance.post('/')
async def create_ambulance(ambulance: Ambulance, token: str = Depends(oauth2_scheme)):
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

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    if(response.json().get('nickname') is not None):
       return  "Ambulance created"
    else:
       return response.json()
    

@ambulance.put('/update/{id}')
async def update_ambulance(id: int, ambulance: Ambulance, token: str = Depends(oauth2_scheme)):
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
    

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    if(response.json().get('nickname') is not None):
       return  "Ambulance updated"
    else:
       return response.json()

@ambulance.put('/set_busy_status/{id}')
async def set_ambulance_as_busy(id: int, token: str = Depends(oauth2_scheme)):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.update().values(
        status = 'Busy'
    ).where(ambulances.c.id == id))

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    if(response.json().get('nickname') is not None):
       return  "Ambulance set as busy"
    else:
       return response.json()
    

@ambulance.put('/make_available/{id}')
async def make_available(id: int, token: str = Depends(oauth2_scheme)):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.update().values(
        status = 'Free'
    ).where(ambulances.c.id == id))
    
    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    if(response.json().get('nickname') is not None):
       return  "Ambulanced made available"
    else:
       return response.json()

@ambulance.put('/exclude/{id}')
async def exclude_ambulance(id: int, token: str = Depends(oauth2_scheme)):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.update().values(
        status = 'Not Available'
    ).where(ambulances.c.id == id))

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    if(response.json().get('nickname') is not None):
       return  "Ambulance excluded"
    else:
       return response.json()
    

@ambulance.delete('/{id}')
async def delete_ambulance(id: int, token: str = Depends(oauth2_scheme)):
    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.id == id)).first()
    if ambulance_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ambulance with this id doesn't exist"
        )
    conn.execute(ambulances.delete().where(ambulances.c.id == id))

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    if(response.json().get('nickname') is not None):
       return  "Ambulance deleted"
    else:
       return response.json()
    
