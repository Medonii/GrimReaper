from fastapi import FastAPI
from routes.patient import patient


app = FastAPI()

app.include_router(patient)
