from fastapi import APIRouter, HTTPException, status
from models.request import requests
from config.db import conn
from schemas.request import Request

request = APIRouter()

@request.get('/')
async def fetch_request():
    return conn.execute(requests.select()).fetchall()

@request.get('/{id}')
async def fetch_request(id: int):
    return conn.execute(requests.select().where(requests.c.id == id)).first()

@request.post('/')
async def create_request(request: Request):
    request_db = conn.execute(requests.select().where(requests.c.name == request.name)).first()
    if request_db is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="request with this name already exist"
        )
    conn.execute(requests.insert().values(
        name = request.name,
        status = request.status,
        address = request.address
    ))
    return  conn.execute(requests.select()).fetchall()

@request.put('/{id}')
async def update_request(id: int, request: Request):
    conn.execute(requests.update().values(
        name = request.name,
        status = request.status,
        address = request.address
    ).where(requests.c.id == id))
    return  conn.execute(requests.select()).fetchall()

@request.delete('/{id}')
async def delete_request(id: int):
    conn.execute(requests.delete().where(requests.c.id == id))
    return  conn.execute(requests.select()).fetchall()
