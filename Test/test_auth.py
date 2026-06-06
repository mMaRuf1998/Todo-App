from jose import jwt

from .utils import *
from ..routers.admin import get_db
from ..routers.auth import authenticate_user , \
    get_current_user, create_access_token,secret_key,algorithm
from fastapi import status
from ..main import app
from datetime import datetime, timedelta
import pytest
from fastapi import HTTPException


app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestSessionLocal()

    true_user = authenticate_user(test_user.username, '1234555', db)
    assert true_user is not None
    assert true_user.username == test_user.username

    fake_user = authenticate_user("asdasd",'asdasdasd',db)
    assert fake_user is False

    wrong_pass_user = authenticate_user(test_user.username, 'asdasd', db)
    assert wrong_pass_user is False

def test_create_token():
    username = 'test_user'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id,role, expires_delta)
    decoded_token = jwt.decode(token, secret_key, algorithm)

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['user_role'] == role

@pytest.mark.asyncio
async def test_get_current_user(test_user):
    encode = {'sub': "test_user" , 'id': 1, 'user_role': 'admin'}
    token = jwt.encode(encode, secret_key, algorithm)

    user = await get_current_user(token)

    assert user == {'username':'test_user', 'user_id': 1, 'user_role': 'admin'}

@pytest.mark.asyncio
async def test_get_current_user_with_missing_payload(test_user):
    encode = {'role': "test_user"}
    token = jwt.encode(encode, secret_key, algorithm)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == 'Could not validate credentials'


