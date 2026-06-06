from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status
from ..models import Users
from ..main import app

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "TestUser"
    assert response.json()["email"] == "maruf1s@gmail.com"
    assert response.json()["first_name"] == "Maruf_TEST"
    assert response.json()["last_name"] == "Ahmed_Test"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "012213123"


def test_change_password(test_user):
    response = client.put("/user/changepassword" , params={
        "oldpassword": "1234555",
        "password": "123232131231231",
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_password_invalid(test_user):
    response = client.put("/user/changepassword", params={
        "oldpassword": "123453355",
        "password": "123232131231231",
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect password"

def test_phone_number_success(test_user):
    response = client.put("/user/phonenumber/12312312")
    assert response.status_code == status.HTTP_200_OK