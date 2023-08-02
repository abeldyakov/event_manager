from tests.conftest import client


def test_participate():
    email = "members_test1@example.com"
    username = "members_test1"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    auth_data = response.json()
    date = "2023-08-02"
    name = "event5"
    description = "description of event5"
    response = client.post(
        "/events",
        headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
        json={
            "date": date,
            "name": name,
            "description": description
        }
    )
    assert response.status_code == 201
    event_data = response.json()

    response = client.get(
        f"/members/{event_data['uuid']}",
        headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
    )
    assert response.status_code == 201
    member_data = response.json()
    assert member_data["event_uuid"] == event_data["uuid"]


def test_already_registered():
    email = "members_test2@example.com"
    username = "members_test2"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    auth_data = response.json()
    date = "2023-08-02"
    name = "event6"
    description = "description of event6"
    response = client.post(
        "/events",
        headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
        json={
            "date": date,
            "name": name,
            "description": description
        }
    )
    assert response.status_code == 201
    event_data = response.json()

    response = client.get(
        f"/members/{event_data['uuid']}",
        headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
    )
    assert response.status_code == 201
    member_data = response.json()
    assert member_data["event_uuid"] == event_data["uuid"]

    response = client.get(
        f"/members/{event_data['uuid']}",
        headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
    )
    assert response.status_code == 409
