from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..database import SessionLocal, get_db
from ..models import Todos
from .auth import get_current_user
router = APIRouter()


class todo_Object(BaseModel):
    title: str = Field(min_length=1,max_length=100)
    description: str = Field(min_length=1,max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool = Field(default=False)


db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    return db.query(Todos).filter(Todos.owner_id==user.get('user_id')).all()

#Find a todo by ID:

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('user_id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")


@router.post("/todos/create", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db:db_dependency, todo_request: todo_Object):

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    newTodo = Todos(**todo_request.model_dump(),owner_id=user.get('user_id'))

    if newTodo is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item not found")
    db.add(newTodo)
    db.commit()

@router.put("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: todo_Object, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('user_id')).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.commit()


@router.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    db.delete(todo_model)
    db.commit()



