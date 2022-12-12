from fastapi import FastAPI
from routes.request import request


app = FastAPI()

app.include_router(request)
