import pytest
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from ..database import Base
from ..models import Todos, Users
from ..main import app
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./TodoApp/testtodosapp.db'


engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool
                       )
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

Base.metadata.create_all(engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'admin', 'user_id': 1 , 'user_role':'admin'}


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


@pytest.fixture
def test_user():
    user = Users(
        email="maruf1s@gmail.com",
        username="TestUser",
        first_name="Maruf_TEST",
        last_name="Ahmed_Test",
        hashed_password=bcrypt_context.hash("1234555"),
        is_active=True,
        role="admin",
        phone_number="012213123"
    )
    db= TestSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

