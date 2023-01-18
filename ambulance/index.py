from fastapi import FastAPI
from routes.ambulance import ambulance
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk


sentry_sdk.init(
    dsn="https://3839abb39a01461d864a6227e9027a54@o4504526357790721.ingest.sentry.io/4504526515929088",

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

app.include_router(ambulance)
