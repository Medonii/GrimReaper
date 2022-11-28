from fastapi import APIRouter, HTTPException, status
from models.user import users
from config.db import conn
from schemas.user import User
from auth.user_auth import get_password_hash


user = APIRouter()

@user.get('/')
async def fetch_users():
    return conn.execute(users.select()).fetchall()

@user.get('/{id}')
async def fetch_user(id: int):
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.post('/')
async def create_user(user: User):
    user_db = conn.execute(users.select().where(users.c.nickname == user.nickname)).first()
    if user_db is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this nickname already exist"
        )
    conn.execute(users.insert().values(
        nickname = user.nickname,
        password = get_password_hash(user.password)
    ))
    return  conn.execute(users.select()).fetchall()

@user.put('/{id}')
async def update_user(id: int, user: User):
    conn.execute(users.update().values(
        nickname = user.nickname,
        password = get_password_hash(user.password)
    ).where(users.c.id == id))
    return  conn.execute(users.select()).fetchall()

@user.delete('/{id}')
async def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return  conn.execute(users.select()).fetchall()

