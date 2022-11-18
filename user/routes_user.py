from fastapi import APIRouter
from user.models_user import users
from user.db import conn
from user.schemas_user import User

user = APIRouter()

@user.get('/')
async def fetch_users():
    return conn.execute(users.select()).fetchall()

@user.get('/{id}')
async def fetch_user(id: int):
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.post('/')
async def create_user(user: User):
    conn.execute(users.insert().values(
        nickname = user.nickname,
        password = user.password
    ))
    return  conn.execute(users.select()).fetchall()

@user.put('/{id}')
async def update_user(id: int, user: User):
    conn.execute(users.update().values(
        nickname = user.nickname,
        password = user.password
    ).where(users.c.id == id))
    return  conn.execute(users.select()).fetchall()

@user.delete('/{id}')
async def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return  conn.execute(users.select()).fetchall()