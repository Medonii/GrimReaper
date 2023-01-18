from fastapi import FastAPI
from routes.user import user
from auth.user_auth import user_auth
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk


sentry_sdk.init(
    dsn="https://9a2968fa1d0b4c8d9185c9f72c10b220@o4504526357790721.ingest.sentry.io/4504526524776448",

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

app.include_router(user)
app.include_router(user_auth)