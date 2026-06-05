import sys
from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal, get_db
from ..models import Users
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from jose import jwt, JWTError

load_dotenv("TodoApp/files.env")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


db_dependency = Annotated[Session,Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str,  user_id:int, user_role: str, expires_delta:timedelta):
    encode = {'sub': username,'id': user_id,'user_role': user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, secret_key, algorithm=algorithm)


class createUserRequest(BaseModel): #You can add validation here using Field/ This is a Pydantic Class/Sample User Input Expectation
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    is_active:bool
    role:str
    phone_number:str

class Token(BaseModel):
    access_token: str
    token_type: str

async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username:str = payload['sub']
        user_id:int = payload['id']
        user_role:str = payload['user_role']

        if username is None or user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='Could not validate credentials')

        return {'username':username,'user_id':user_id , 'user_role':user_role}

    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='Could not validate credentials')


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,newUserRequest:createUserRequest):
    newUser = Users(
        email=newUserRequest.email,
        username=newUserRequest.username,
        first_name=newUserRequest.first_name,
        last_name=newUserRequest.last_name,
        hashed_password=bcrypt_context.hash(newUserRequest.password),
        is_active = newUserRequest.is_active,
        role = newUserRequest.role,
        phone_number=newUserRequest.phone_number
    )
    db.add(newUser)
    db.commit()

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='Could not validate credentials')

    token = create_access_token(user.username, user.id,user.role, timedelta(minutes=20))

    return {'access_token':token, 'token_type': 'bearer'}