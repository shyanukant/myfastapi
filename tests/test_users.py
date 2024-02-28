# testcases for users and login rourter

import pytest
from jose import jwt
from app import schemas
from app.config import settings


# Test root route
def test_root(client):
    res = client.get("/")
    assert res.status_code == 200

# Test user registration
def test_login_user(test_user, client):
    data = {
        "username": test_user['email'],
        "password": test_user['password']
    }
    res = client.post("/login", data=data)
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

# test case if user credentials are incorrect
@pytest.mark.parametrize("email, password, status_code", [
    ("wrong_email", "wrong_password", 403),
    ("myemail@gmail.com", "wrong_password", 403),
    ("testshyanukant@gmail.com", None, 422),
    (None, "password", 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code

def test_authorized_get_all_users(authorized_client, test_user, test_user2):
    res = authorized_client.get("/users/")
    assert len(res.json()) == 2
    assert res.status_code == 200

def test_get_all_users(client, test_user, test_user2):
    res = client.get("/users/")
    assert len(res.json()) == 2
    assert res.status_code == 200

def test_get_all_users_non_exist(client):
    res = client.get("/users/")
    assert res.status_code == 404

def test_authorized_get_user_by(authorized_client, test_user2):
    res = authorized_client.get(f"/users/{test_user2['id']}")
    assert res.status_code == 200

def test_get_all_user_by(client, test_user2):
    res = client.get(f"/users/{test_user2['id']}")
    assert res.status_code == 200

def test_get_user_id_non_exist(client):
    res = client.get("/users/8878787")
    assert res.status_code == 404

def test_delete_user_success(authorized_client, test_user):
    res = authorized_client.delete(f"/users/{test_user['id']}")
    assert res.status_code == 204

def test_delete_user_not_owner(authorized_client, test_user2):
    res = authorized_client.delete(f"/users/{test_user2['id']}")
    assert res.status_code == 401

def test_unauthorized_delete_user(client, test_user):
    res = client.delete(f"/users/{test_user['id']}")
    assert res.status_code == 401

def test_update_user_success(authorized_client, test_user):
    data = {
        "email": "updatedemail@gmail.com",
        "phone": "8989898988",
        "password": "updatepass"
    }
    res = authorized_client.put(f"/users/{test_user['id']}", json=data)
    assert res.status_code == 200

def test_update_user_not_owner(authorized_client, test_user2):
    data = {
        "email": "updatedemail@gmail.com",
        "phone": "8989898988",
        "password": "updatepass"
    }
    res = authorized_client.put(f"/users/{test_user2['id']}", json=data)
    assert res.status_code == 401

def test_unauthorized_update_user(client, test_user):
    data = {
        "email": "updatedemail@gmail.com",
        "phone": "8989898988",
        "password": "updatepass"
    }
    res = client.put(f"/users/{test_user['id']}", json=data)
    assert res.status_code == 401

