from fastapi import FastAPI
from user.routes_user import user

app = FastAPI()

app.include_router(user)