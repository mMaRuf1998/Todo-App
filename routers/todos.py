from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path,Request
from ..database import SessionLocal, get_db
from ..models import Todos
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
router = APIRouter(
    prefix='/todos',
    tags=['todos'],
)

templates = Jinja2Templates(directory="TodoApp/templates")

class todo_Object(BaseModel):
    title: str = Field(min_length=1,max_length=100)
    description: str = Field(min_length=1,max_length=100)
    priority: int = Field(gt=0,lt=6)
    complete: bool = Field(default=False)


db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)

    return redirect_response




@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    return db.query(Todos).filter(Todos.owner_id==user.get('user_id')).all()

#Find a todo by ID:
@router.get("/todo-page",status_code=status.HTTP_200_OK)
async def render_all_todo(request: Request, db: db_dependency):
        try:
            user = await get_current_user(request.cookies.get("access_token"))
            if user is None:
                return redirect_to_login()

            todos = db.query(Todos).filter(Todos.owner_id==user.get('user_id')).all()

            return templates.TemplateResponse(request=request,name="todos.html",context={"todos": todos, "user": user})
        except:
            return redirect_to_login()

@router.get("/add-todo-page",status_code=status.HTTP_200_OK)
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(request=request , name="add-todo.html" , context={"user": user})
    except:
        return redirect_to_login()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('user_id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db:db_dependency, todo_request: todo_Object):

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    newTodo = Todos(**todo_request.model_dump(),owner_id=user.get('user_id'))

    if newTodo is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item not found")
    db.add(newTodo)
    db.commit()

@router.put("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
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


@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    db.delete(todo_model)
    db.commit()



