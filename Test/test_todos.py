import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

#from TodoApp.main import app
from ..database import Base
from ..main import app
from ..routers.auth import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from ..models import Todos

SQLALCHEMY_DATABASE_URL = 'sqlite:///./TodoApp/testtodosapp.db'


engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool
                       )
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'admin', 'user_id': 1 , 'user_role':'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user
client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Need to code",
        priority=3,
        complete=False,
        owner_id=1
    )
    db= TestSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    print(response.json)
    assert response.json() == [{
        'complete': False,
        'title':'Learn to code',
    'description' : 'Need to code',
    'priority' : 3,
    'owner_id' : 1,
        'id':1
    }]



def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    print(response.json)
    assert response.json() == {
        'complete': False,
        'title':'Learn to code',
    'description' : 'Need to code',
    'priority' : 3,
    'owner_id' : 1,
        'id':1
    }


def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}


def test_create_todo(test_todo):
    request_data = {
    'title': 'New Todo',
    'description':'Description',
    'priority': 5,
    'complete': False
    }

    response = client.post("/todos/create", json=request_data)
    assert response.status_code == 201
    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.complete == request_data['complete']


def test_update_todo(test_todo):
    request_data = {
        'title':'Changed Title',
        'description':'Changed Description',
        'priority': 1,
        'complete': False
    }
    response = client.put("/todos/1", json=request_data)
    assert response.status_code == 204
    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    assert model.title == "Changed Title"


def test_update_todo_not_found(test_todo):
    request_data = {
        'title':'Changed Title',
        'description':'Changed Description',
        'priority': 1,
        'complete': False
    }
    response = client.put("/todos/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail':"Item not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todos/1")
    assert response.status_code == 204
    db = TestSessionLocal()
    model= db.query(Todos).filter(Todos.id==1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail':"Item not found"}

