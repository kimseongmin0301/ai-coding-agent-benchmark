def test_list_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_existing_user(client):
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"


def test_get_missing_user(client):
    response = client.get("/users/999")

    assert response.status_code == 404


def test_create_user(client):
    response = client.post(
        "/users",
        json={"name": "Charlie", "email": "charlie@example.com"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "name": "Charlie",
        "email": "charlie@example.com",
    }


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == 204

    response = client.get("/users/1")
    assert response.status_code == 404


def test_create_user_with_duplicate_email_returns_409(client):
    response = client.post(
        "/users",
        json={"name": "Alice Clone", "email": "alice@example.com"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"

    # the rejected request must not add or modify anything
    assert len(client.get("/users").json()) == 2
    assert client.get("/users/1").json()["name"] == "Alice"


def test_create_user_with_duplicate_email_ignores_case(client):
    response = client.post(
        "/users",
        json={"name": "Alice Clone", "email": "ALICE@example.com"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"
    assert len(client.get("/users").json()) == 2


def test_create_user_after_delete_does_not_reuse_existing_id(client):
    assert client.delete("/users/1").status_code == 204

    response = client.post(
        "/users",
        json={"name": "Charlie", "email": "charlie@example.com"},
    )

    assert response.status_code == 201
    assert response.json()["id"] not in (1, 2)

    # the surviving user must not be overwritten
    assert client.get("/users/2").json() == {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
    }
    assert len(client.get("/users").json()) == 2


def test_create_user_with_new_email_returns_201(client):
    response = client.post(
        "/users",
        json={"name": "Dana", "email": "dana@example.com"},
    )

    assert response.status_code == 201

    body = response.json()
    assert body["name"] == "Dana"
    assert body["email"] == "dana@example.com"
    assert client.get(f"/users/{body['id']}").status_code == 200


def test_create_user_preserves_email_casing(client):
    response = client.post(
        "/users",
        json={"name": "Erin", "email": "Erin@Example.com"},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "Erin@Example.com"
