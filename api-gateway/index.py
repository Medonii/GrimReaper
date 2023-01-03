from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from fastapi_gateway import route
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import APIKeyHeader
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException
from schemas.gateway import User, UserBody, Token, Ambulance, AmbulanceBody, Patient

app = FastAPI(title='API Gateway')

SERVICE_URL_USER = "http://user:80"
SERVICE_URL_AMBULANCE = "http://ambulance:8000"
SERVICE_URL_PATIENT = "http://patient:8008"

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=False
)


def check_api_key(key: str = Depends(api_key_header)):
    if key:
        return key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You didn't pass the api key in the header! Header: x-api-key",
    )


@route(
    request_method=app.get,
    service_url=SERVICE_URL_USER,
    gateway_path='/users/{id}',
    service_path='/{id}',
    status_code=status.HTTP_200_OK,
    override_headers=False,
    response_model=User,
    query_params=["id"],
)
async def check_query_params_and_body(
        id: int, request: Request, response: Response
):
    pass


@route(
    request_method=app.post,
    service_url=SERVICE_URL_USER,
    gateway_path='/users/create',
    service_path='/',
    status_code=status.HTTP_200_OK,
    body_params=["test_body"],
    response_model=str,
)
async def check_query_params_and_body(
        request: Request, 
        response: Response,
        test_body: UserBody,
):
    pass

@route(
    request_method=app.put,
    service_url=SERVICE_URL_USER,
    gateway_path='/users/update_user/{id}',
    service_path='/{id}',
    status_code=status.HTTP_200_OK,
    body_params=["test_body"],
    response_model=str,
)
async def check_query_params_and_body(
        request: Request, 
        response: Response,
        test_body: UserBody,
):
    pass


@route(
    request_method=app.delete,
    service_url=SERVICE_URL_USER,
    gateway_path='/users/delete_user/{id}',
    service_path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
    query_params=["id"],
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass


@route(
    request_method=app.post,
    service_url=SERVICE_URL_USER,
    gateway_path='/users/token',
    service_path='/token',
    status_code=status.HTTP_200_OK,
    form_params=['user_in'],
    response_model=Token,
 
)
async def check_query_params_and_body(
        request: Request, 
        response: Response,
        user_in: OAuth2PasswordRequestForm = Depends(),
):
    pass


@route(
    request_method=app.get,
    service_url=SERVICE_URL_AMBULANCE,
    gateway_path='/ambulances/{id}',
    service_path='/{id}',
    status_code=status.HTTP_200_OK,
    override_headers=False,
    response_model=Ambulance,
    query_params=["id"],
)
async def check_query_params_and_body(
        id: int, request: Request, response: Response
):
    pass

@route(
    request_method=app.post,
    service_url=SERVICE_URL_AMBULANCE,
    gateway_path='/ambulances/create',
    service_path='/',
    status_code=status.HTTP_200_OK,
    body_params=["test_body"],
    response_model=str,
)
async def check_query_params_and_body(
        request: Request, 
        response: Response,
        test_body: AmbulanceBody,
):
    pass


@route(
    request_method=app.put,
    service_url=SERVICE_URL_AMBULANCE,
    gateway_path='/ambulances/update_ambulance/{id}',
    service_path='/{id}',
    status_code=status.HTTP_200_OK,
    body_params=["test_body"],
    response_model=str,
)
async def check_query_params_and_body(
        request: Request, 
        response: Response,
        test_body: AmbulanceBody,
):
    pass

@route(
    request_method=app.delete,
    service_url=SERVICE_URL_AMBULANCE,
    gateway_path='/ambulances/delete_ambulance/{id}',
    service_path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
    query_params=["id"],
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass


@route(
    request_method=app.put,
    service_url=SERVICE_URL_AMBULANCE,
    gateway_path='/ambulances/set_busy_status/{id}',
    service_path='/set_busy_status/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass

@route(
    request_method=app.put,
    service_url=SERVICE_URL_AMBULANCE,
    gateway_path='/ambulances/make_available/{id}',
    service_path='/make_available/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass


@route(
    request_method=app.put,
    service_url=SERVICE_URL_AMBULANCE,
    gateway_path='/ambulances/exclude/{id}',
    service_path='/exclude/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass


@route(
    request_method=app.get,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/{id}',
    service_path='/fetch/{id}',
    status_code=status.HTTP_200_OK,
    override_headers=False,
    response_model=Patient,
    query_params=["id"],
)
async def check_query_params_and_body(
        id: int, request: Request, response: Response
):
    pass


@route(
    request_method=app.post,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/create',
    service_path='/create',
    status_code=status.HTTP_200_OK,
    body_params=["test_body"],
    response_model=str,
)
async def check_query_params_and_body(
        request: Request, 
        response: Response,
        test_body: Patient,
):
    pass


@route(
    request_method=app.put,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/update/{id}',
    service_path='/update/{id}',
    status_code=status.HTTP_200_OK,
    body_params=["test_body"],
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
        test_body: Patient,
):
    pass


@route(
    request_method=app.delete,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/delete/{id}',
    service_path='/delete/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
    query_params=["id"],
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass


@route(
    request_method=app.put,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/accept/{id}',
    service_path='/accept/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass

@route(
    request_method=app.put,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/reject/{id}',
    service_path='/reject/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass

@route(
    request_method=app.put,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/start/{id}',
    service_path='/start/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass

@route(
    request_method=app.put,
    service_url=SERVICE_URL_PATIENT,
    gateway_path='/patients/close/{id}',
    service_path='/close/{id}',
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def check_query_params_and_body(
        id: int,
        request: Request, 
        response: Response,
):
    pass