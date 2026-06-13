
from fastapi import FastAPI, Request,status
from starlette.status import HTTP_200_OK

from .models import Base
from .database import engine
from .routers import auth,todos,admin,users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse



app = FastAPI()
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy", status_code=HTTP_200_OK)
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)  #Connecting with authentication api endpoint
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)



