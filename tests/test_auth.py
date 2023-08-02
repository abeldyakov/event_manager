import pytest

from tests.conftest import client


def test_read_main():
    response = client.get("/docs")
    assert response.status_code == 200


def test_sigt_up():
    responce = client.post("/auth/sign-up/", json={
                                  "email": "user@example.com",
                                  "username": "string",
                                  "password": "string"
                                }
                           )
    assert responce.status_code == 201


def test_sign_in():
    response = client.post("/auth/sign-in/", json={"username": "user@example.com", "password": "string"},
                           headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "token_type" == "bearer"
    return response_data["token_type"], response_data["access_token"]
