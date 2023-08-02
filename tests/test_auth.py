import json
import uuid

from jose import jwt

import settings
from tests.conftest import client


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404


def test_sign_up():
    email = "user1@example.com"
    username = "user1"
    password = "password"
    # testing sigt_up
    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           }
                           )
    assert response.status_code == 201
    data = response.json()

    payload = jwt.decode(
        data["access_token"],
        settings.settings.jwt_secret,
        algorithms=[settings.settings.jwt_algorithm],
    )
    user_data = json.loads(payload.get('user'))
    assert user_data.get('username') == username
    assert user_data.get('email') == email
    assert data["token_type"] == "bearer"

    # testing sign-in
    response = client.post(
        "/auth/sign-in/", data={"username": email, "password": password}
    )
    assert response.status_code == 200, response.text


def test_sigt_in():
    email = "user2@example.com"
    username = "user2"
    password = "string"
    # testing sigt_up
    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })

    response = client.post(
        "/auth/sign-in/", data={"username": email, "password": password}
    )
    assert response.status_code == 200, response.text


def test_unauthorized_profile():
    response = client.get("/auth/profile/")
    assert response.status_code == 401


def test_profile():
    email = "test3@example.com"
    username = "test3"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    data = response.json()
    response = client.get("/auth/profile/", headers={
        "Authorization": data["token_type"] + " " + data["access_token"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email
    assert uuid.UUID(data["uuid"]).version == 4


def test_user_exist():
    email = "test4@example.com"
    username = "test4"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    assert response.status_code == 201
    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    assert response.status_code == 409
