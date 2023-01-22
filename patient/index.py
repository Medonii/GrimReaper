from fastapi import FastAPI
from routes.patient import patient
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk


sentry_sdk.init(
    dsn="https://4641d65e879c48f7880dc4e3cdb822fb@o4504526357790721.ingest.sentry.io/4504526523138048",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient)
