from datetime import datetime, timedelta
from typing import List, Union

from fastapi import Depends, HTTPException, status, APIRouter, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from pydantic import BaseModel, ValidationError
from config.db import conn
from models.user import users
from schemas.user import User

from jose import JWTError, jwt
from passlib.context import CryptContext
import sentry_sdk



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"admin": "Do everything.", "operator": "Operate requests", "ambulance_driver": "Read requests, update ambulance."},
    )

user_auth = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(nickname: str):
    user_db: User
    user_db = conn.execute(users.select().where(users.c.nickname == nickname)).first()
    if user_db is not None:
        return user_db


def authenticate_user(nickname: str, password: str):
    user = get_user(nickname)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nickname: str = payload.get("sub")
        if nickname is None:
            raise 
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=nickname)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(nickname=token_data.username)
    if user is None:
        sentry_sdk.capture_exception(Exception("HTTP_401_UNAUTHORIZED, Could not validate credentials"))
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            sentry_sdk.capture_exception(Exception("HTTP_401_UNAUTHORIZED, Not enough permissions"))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )    
    return user


@user_auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        sentry_sdk.capture_exception(Exception("HTTP_401_UNAUTHORIZED, Incorrect nickname or password"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect nickname or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nickname, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_auth.post('/register')
async def create_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = conn.execute(users.select().where(users.c.nickname == form_data.username)).first()
    if user_db is not None:
            sentry_sdk.capture_exception(Exception("HTTP_401_UNAUTHORIZED, User with this nickname already exists"))
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this nickname already exists"
        )
    conn.execute(users.insert().values(
        nickname = form_data.username,
        password = get_password_hash(form_data.password)
    ))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_auth.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@user_auth.get("/users/me/items/")
async def read_own_items(current_user: User = Security(get_current_user, scopes=["operator"])):
    return [{"item_id": "Foo", "owner": current_user.nickname}]

