from fastapi import FastAPI
from routes.ambulance_search import user

app = FastAPI()

app.include_router(ambulance_search)