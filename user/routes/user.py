from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from models.user import users
from config.db import conn
from schemas.user import User
from auth.user_auth import get_password_hash
import sentry_sdk


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"admin": "Do everything.", "operator": "Operate requests", "ambulance_driver": "Read requests, update ambulance."},
    )

user = APIRouter()

@user.get('/')
async def fetch_users(token: str = Depends(oauth2_scheme)):

    return conn.execute(users.select()).fetchall()


@user.get('/{id}')
async def fetch_user(id: int, token: str = Depends(oauth2_scheme)):

    return conn.execute(users.select().where(users.c.id == id)).first()

@user.post('/')
async def create_user(user: User, token: str = Depends(oauth2_scheme)):
    user_db = conn.execute(users.select().where(users.c.nickname == user.nickname)).first()
    if user_db is not None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, User with this nickname already exists"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this nickname already exists"
        )
    conn.execute(users.insert().values(
        nickname = user.nickname,
        password = get_password_hash(user.password),
        role = "Operator"
    ))
    return  "User created"

@user.put('/{id}')
async def update_user(id: int, user: User, token: str = Depends(oauth2_scheme)):
    user_db = conn.execute(users.select().where(users.c.id == id)).first()
    if user_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, User with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this id doesn't exist"
        )
    conn.execute(users.update().values(
        nickname = user.nickname,
        password = get_password_hash(user.password),
        role = user.role,
        ambulance = user.ambulance
    ).where(users.c.id == id))
    return  "User updated"

@user.delete('/{id}')
async def delete_user(id: int, token: str = Depends(oauth2_scheme)):
    user_db = conn.execute(users.select().where(users.c.id == id)).first()
    if user_db is None:
            sentry_sdk.capture_exception(Exception("HTTP_400_BAD_REQUEST, User with this id doesn't exist"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this id doesn't exist"
        )
    conn.execute(users.delete().where(users.c.id == id))
    return  "User deleted"

