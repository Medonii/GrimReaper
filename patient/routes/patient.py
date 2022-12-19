from fastapi import APIRouter, HTTPException, status, Request
from models.patient import patients
from config.db import conn
from schemas.patient import Patient
import requests, json

patient = APIRouter()

@patient.get('/')
async def fetch_patient():
    return conn.execute(patients.select()).fetchall()

@patient.get('/fetch/{id}')
async def fetch_patient(id: int):
    return conn.execute(patients.select().where(patients.c.id == id)).first()

@patient.post('/create')
async def create_patient(patient: Patient):
    patient_db = conn.execute(patients.select().where(patients.c.name == patient.name)).first()
    if patient_db is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient request with this name already exists."
        )
    conn.execute(patients.insert().values(
        name = patient.name,
        status = "Registered",
        address = patient.address
    ))
    return  conn.execute(patients.select()).fetchall()

@patient.put('/update/{id}')
async def update_patient(id: int, patient: Patient):
    conn.execute(patients.update().values(
        name = patient.name,
        address = patient.address
    ).where(patients.c.id == id))
    return  conn.execute(patients.select()).fetchall()

@patient.delete('/delete/{id}')
async def delete_patient(id: int):
    conn.execute(patients.delete().where(patients.c.id == id))
    return  conn.execute(patients.select()).fetchall()

@patient.put('/accept/{id}')
async def accept_patient(id: int):

    url = 'http://ambulance:8000/'
    response = requests.get(url)
    data = response.json()

    conn.execute(patients.update().values(
        status = "Ambulance Assigned",
        ambulance = data[0]['tag']
    ).where(patients.c.id == id))

    requests.put('http://ambulance:8000/set_busy_status/1')

    return  conn.execute(patients.select()).fetchall()

@patient.put('/reject/{id}')
async def reject_patient(id: int, patient: Patient):
    conn.execute(patients.update().values(
        status = "Rejected",
        ambulance = None
    ).where(patients.c.id == id))
    return  conn.execute(patients.select()).fetchall()

@patient.put('/start/{id}')
async def start_patient(id: int, patient: Patient):
    conn.execute(patients.update().values(
        status = "In Progress"
    ).where(patients.c.id == id))
    return  conn.execute(patients.select()).fetchall()
