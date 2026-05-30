from fastapi import APIRouter
from pydantic import BaseModel

from models import Users

router = APIRouter()

class createUserRequest(BaseModel): #You can add validation here using Field/ This is a Pydantic Class/Sample User Input Expectation
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    is_active:bool
    role:str

@router.post("/auth")
async def create_user(newUserRequest:createUserRequest):
    newUser = Users(
        email=newUserRequest.email,
        username=newUserRequest.username,
        first_name=newUserRequest.first_name,
        last_name=newUserRequest.last_name,
        hashed_password=newUserRequest.password,
        is_active = newUserRequest.is_active,
        role = newUserRequest.role
    )

    return newUser
