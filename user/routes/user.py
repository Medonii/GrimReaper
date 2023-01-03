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
            detail="User with this nickname already exists"
        )
    conn.execute(users.insert().values(
        nickname = user.nickname,
        password = get_password_hash(user.password)
    ))
    return  "User created"

@user.put('/{id}')
async def update_user(id: int, user: User):
    user_db = conn.execute(users.select().where(users.c.id == id)).first()
    if user_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this id doesn't exist"
        )
    conn.execute(users.update().values(
        nickname = user.nickname,
        password = get_password_hash(user.password)
    ).where(users.c.id == id))
    return  "User updated"

@user.delete('/{id}')
async def delete_user(id: int):
    user_db = conn.execute(users.select().where(users.c.id == id)).first()
    if user_db is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this id doesn't exist"
        )
    conn.execute(users.delete().where(users.c.id == id))
    return  "User deleted"

