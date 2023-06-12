from typing import Union
from ambulance.models.ambulance import ambulances
from fastapi import APIRouter, HTTPException, status, Request, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from models.patient import patients
from config.db import conn
from schemas.patient import Patient
import requests, json
from models.import_api import get_api_key
import gmaps
import googlemaps
from datetime import datetime
import sentry_sdk

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://user-service:80/token",
    scopes={"admin": "Do everything.", "operator": "Operate requests", "ambulance_driver": "Read requests, update ambulance."},
    )

patient = APIRouter()

@patient.get('/')
async def fetch_patient(ambulance: Union[str, None] = None, token: str = Depends(oauth2_scheme)):

    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        if ambulance: return conn.execute(patients.select().where(patients.c.ambulance == ambulance)).fetchall()
        else:
            return conn.execute(patients.select()).fetchall()
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_UNAUTHORIZED, Not authorized"))
        return response.json()
        

@patient.get('/fetch/{id}')
async def fetch_patient(id: int, token: str = Depends(oauth2_scheme)):
    return conn.execute(patients.select().where(patients.c.id == id)).first()

@patient.post('/create')
async def create_patient(patient: Patient, token: str = Depends(oauth2_scheme)):
    patient_db = conn.execute(patients.select().where(patients.c.name == patient.name)).first()
    if patient_db is not None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, Patient request with this name already exists."))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient request with this name already exists."
        )
    conn.execute(patients.insert().values(
        name = patient.name,
        status = "Registered",
        address = patient.address,
        type = patient.type
    ))

    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        return  "Patient created"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_UNAUTHORIZED, Not authorized"))
        return response.json()

@patient.put('/update/{id}')
async def update_patient(id: int, patient: Patient, token: str = Depends(oauth2_scheme)):
    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, patient with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )
    conn.execute(patients.update().values(
        name = patient.name,
        address = patient.address,
        ambulance = patient.ambulance,
        people = patient.people,
        type = patient.type
    ).where(patients.c.id == id))

    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        return "Patient updated"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_BAD_REQUEST, Not authorized"))
        return response.json()

@patient.delete('/delete/{id}')
async def delete_patient(id: int, token: str = Depends(oauth2_scheme)):
    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, patient with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )
    conn.execute(patients.delete().where(patients.c.id == id))

    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        return  "Patient deleted"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_BAD_REQUEST, Not authorized"))
        return response.json()

@patient.put('/suggest/{id}')
async def suggest_patient_ambulance(id: int, token: str = Depends(oauth2_scheme)):

    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, patient with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )
    url = 'http://ambulance-service:8000/'
    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    data = response.text
    parsed = json.loads(data)

    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    address = patient_db.address

    route_time = 0

    for ambulance in parsed:
        if ambulance['status'] == 'Free' and ambulance['type'] == patient_db.type:
            if route_time==0:
                route_time = get_time(ambulance['position'], address)
                selected = ambulance
            else:
                if route_time > get_time(ambulance['position'], address):
                    route_time = get_time(ambulance['position'], address)
                    selected = ambulance

    if route_time == 0:
        for ambulance in parsed:
            if ambulance['status'] == 'Free':
                if route_time==0:
                    route_time = get_time(ambulance['position'], address)
                    selected = ambulance
                else:
                    if route_time > get_time(ambulance['position'], address):
                        route_time = get_time(ambulance['position'], address)
                        selected = ambulance

    if route_time==0:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No free ambulances."
        )

    conn.execute(patients.update().values(
        status = "Ambulance Assigned",
        ambulance = selected['tag']
    ).where(patients.c.id == id))

    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        return  "Ambulance suggestion made"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_BAD_REQUEST, Not authorized"))
        return response.json()

@patient.put('/accept/{id}')
async def accept_patient(id: int, token: str = Depends(oauth2_scheme)):

    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, patient with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )

    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()

    conn.execute(patients.update().values(
        status = "Ambulance Assigned"
    ).where(patients.c.id == id))

    url = 'http://ambulance-service:8000/'
    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    data = response.text
    parsed = json.loads(data)

    for ambulance in parsed:
        if ambulance['tag'] == patient_db.ambulance:
            selected = ambulance

    requests.put('http://ambulance-service:8000/set_busy_status/' + str(selected['id']), headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })


    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        return  "Patient accepted"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_BAD_REQUEST, Not authorized"))
        return response.json()

@patient.put('/set/{id}')
async def set_patient(id: int, ambulance: str, token: str = Depends(oauth2_scheme)):
    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )

    conn.execute(patients.update().values(
        status = "Ambulance Assigned",
        ambulance = ambulance
    ).where(patients.c.id == id))

    url = 'http://user:80/users/me'

    response = requests.get(url, headers={
        "Content-Type": "application/json",
        'Authorization': "Bearer " + token,
    })

    if(response.json().get('nickname') is not None):
        return "Patient updated"
    else:
        return response.json()

@patient.put('/reject/{id}')
async def reject_patient(id: int, token: str = Depends(oauth2_scheme)):
    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, patient with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )

    ambulance_db = conn.execute(ambulances.select().where(ambulances.c.tag == patient_db.ambulance)).first()
    requests.put('http://ambulance-service:8000/make_available/' + str(ambulance_db['id']), headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })

    conn.execute(patients.update().values(
        status = "Rejected",
        ambulance = None
    ).where(patients.c.id == id))

    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        return  "Patient rejected"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_BAD_REQUEST, Not authorized"))
        return response.json()

@patient.put('/start/{id}')
async def start_patient(id: int, token: str = Depends(oauth2_scheme)):
    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, patient with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )
    conn.execute(patients.update().values(
        status = "In Progress"
    ).where(patients.c.id == id))

    url = 'http://user-service:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    
    if(response.json().get('nickname') is not None):
        return  "Patient in progress"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_BAD_REQUEST, Not authorized"))
        return response.json()

@patient.put('/close/{id}')
async def start_patient(id: int, token: str = Depends(oauth2_scheme)):
    patient_db = conn.execute(patients.select().where(patients.c.id == id)).first()
    if patient_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, patient with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient with this id doesn't exist"
        )
    conn.execute(patients.update().values(
        status = "Finished"
    ).where(patients.c.id == id))

    url = 'http://user:80/users/me'

    response = requests.get(url, headers= {
                       "Content-Type": "application/json",
                       'Authorization': "Bearer " + token,
                   })
    

    if(response.json().get('nickname') is not None):
        return  "Patient finished"
    else:
        sentry_sdk.capture_exception(Exception("HTTP_401_BAD_REQUEST, Not authorized"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized"
        )

api_key = get_api_key()
gmaps.configure(api_key)

def get_time(origin , dest):
    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    direction_result = gmaps.directions(origin, dest, mode="driving", avoid="ferries", departure_time=now)
    print(direction_result[0]['legs'][0]['duration']['text'])
    return direction_result[0]['legs'][0]['duration']['value']