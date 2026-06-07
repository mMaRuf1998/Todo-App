
from fastapi import FastAPI, Request
from starlette.status import HTTP_200_OK

from .models import Base
from .database import engine
from .routers import auth,todos,admin,users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



app = FastAPI()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="TodoApp/templates")
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")
templates.env.globals["url_for"] = app.url_path_for


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse({"request": request}, "home.html" )


@app.get("/healthy", status_code=HTTP_200_OK)
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)  #Connecting with authentication api endpoint
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)



