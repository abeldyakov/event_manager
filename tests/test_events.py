import uuid

import settings
from tests.conftest import client


def test_get_empty_events():
    email = "event_test1@example.com"
    username = "event_test1"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    data = response.json()
    response = client.get("/events", headers={
        "Authorization": data["token_type"] + " " + data["access_token"]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_create_event():
    email = "event_test2@example.com"
    username = "event_test2"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    data = response.json()
    date = "2023-08-02"
    name = "event1"
    description = "description of event1"
    response = client.post("/events",
                           headers={"Authorization": data["token_type"] + " " + data["access_token"]},
                           json={
                               "date": date,
                               "name": name,
                               "description": description
                           }
    )
    assert response.status_code == 201
    data = response.json()
    assert uuid.UUID(data["uuid"]).version == 4
    assert data["date"] == date
    assert data["name"] == name
    assert data["description"] == description


def test_get_event():
    email = "event_test3@example.com"
    username = "event_test3"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    auth_data = response.json()
    date = "2023-08-02"
    name = "event2"
    description = "description of event2"
    response = client.post("/events",
                           headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
                           json={
                               "date": date,
                               "name": name,
                               "description": description
                           }
    )
    assert response.status_code == 201
    event_data = response.json()

    response = client.get(f"/events/{event_data['uuid']}",
                          headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
                         )

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == event_data["uuid"]
    assert data["name"] == name
    assert data["description"] == description
    assert len(data["users"]) == 0


def test_update_event():
    email = "event_test4@example.com"
    username = "event_test4"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    auth_data = response.json()
    date = "2023-08-02"
    name = "event3"
    description = "description of event3"
    response = client.post("/events",
                           headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
                           json={
                               "date": date,
                               "name": name,
                               "description": description
                           }
    )
    assert response.status_code == 201
    event_data = response.json()

    response = client.get("/events",
                          headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
                          params={"event_uuid": event_data["uuid"]}
                         )

    assert response.status_code == 200
    data = response.json()[0]
    assert data["uuid"] == event_data["uuid"]
    assert data["name"] == name
    assert data["description"] == description
    assert data["members_count"] == 0
    response = client.put(f"/events/{data['uuid']}",
                          headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
                          json={
                              "date": date,
                              "name": "new name",
                              "description": description
                          }
                         )
    response.status_code = 200
    new_event_data = response.json()
    assert new_event_data["uuid"] == event_data["uuid"]


def test_delete_event():
    email = "event_test5@example.com"
    username = "event_test5"
    password = "string"

    response = client.post("/auth/sign-up/",
                           json={
                               "email": email,
                               "username": username,
                               "password": password
                           })
    auth_data = response.json()
    date = "2023-08-02"
    name = "event4"
    description = "description of event4"
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
        f"/events/{event_data['uuid']}",
        headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
    )

    assert response.status_code == 200
    data = response.json()
    response = client.delete(
        f"/events/{data['uuid']}",
        headers={"Authorization": auth_data["token_type"] + " " + auth_data["access_token"]},
    )
    assert response.status_code == 204
