from fastapi import FastAPI
from routes.ambulance import ambulance


app = FastAPI()

app.include_router(ambulance)
