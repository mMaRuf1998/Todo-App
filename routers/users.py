from idlelib.query import Query
from typing import Annotated

from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query

from database import SessionLocal
from models import Todos,Users
from .auth import get_current_user
router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class todo_Object(BaseModel):
    title: str = Field(min_length=1,max_length=100)
    description: str = Field(min_length=1,max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool = Field(default=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get('/',status_code=status.HTTP_200_OK)
async def get_userinfo(user: user_dependency, db: db_dependency):
    userData = db.query(Users).filter(Users.id==user.get('user_id')).first()

    if userData is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return userData

@router.put('/changepassword',status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency, oldpassword: str, password : Annotated[str, Query(min_length=6)]):
    userData = db.query(Users).filter(Users.id==user.get('user_id')).first()

    if userData is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not bcrypt_context.verify(oldpassword, userData.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")


    userData.hashed_password = bcrypt_context.hash(password)
    db.commit()

    return userData

@router.put("/phonenumber/{phonenumber}",status_code=status.HTTP_200_OK)
async def change_phonenumber(user: user_dependency,db:db_dependency, phonenumber: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    user_model = db.query(Users).filter(Users.id==user.get('user_id')).first()
    user_model.phone_number = phonenumber
    db.add(user_model)
    db.commit()