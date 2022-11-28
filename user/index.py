from fastapi import FastAPI
from routes.user import user
from auth.user_auth import user_auth

app = FastAPI()

app.include_router(user)
app.include_router(user_auth)