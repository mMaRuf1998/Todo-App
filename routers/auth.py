import sys
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

class createUserRequest(BaseModel): #You can add validation here using Field/ This is a Pydantic Class/Sample User Input Expectation
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    is_active:bool
    role:str

@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      newUserRequest:createUserRequest):
    newUser = Users(
        email=newUserRequest.email,
        username=newUserRequest.username,
        first_name=newUserRequest.first_name,
        last_name=newUserRequest.last_name,
        hashed_password=bcrypt_context.hash(newUserRequest.password),
        is_active = newUserRequest.is_active,
        role = newUserRequest.role
    )
    db.add(newUser)
    db.commit()

