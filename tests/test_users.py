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


def test_create_user_rejects_duplicate_email(client):
    response = client.post(
        "/users",
        json={"name": "Alice Copy", "email": "alice@example.com"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_create_user_rejects_duplicate_email_case_insensitive(client):
    response = client.post(
        "/users",
        json={"name": "Alice Upper", "email": "ALICE@example.com"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_create_user_after_delete_does_not_reuse_existing_id(client):
    delete_response = client.delete("/users/1")
    assert delete_response.status_code == 204

    create_response = client.post(
        "/users",
        json={"name": "Charlie", "email": "charlie@example.com"},
    )

    assert create_response.status_code == 201
    assert create_response.json()["id"] == 3

    existing_response = client.get("/users/2")
    assert existing_response.status_code == 200
    assert existing_response.json()["email"] == "bob@example.com"


def test_search_users_by_email_partial_match(client):
    response = client.get("/users/search", params={"email": "alice"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Alice", "email": "alice@example.com"}
    ]


def test_search_users_by_email_case_insensitive(client):
    response = client.get("/users/search", params={"email": "ALICE"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Alice", "email": "alice@example.com"}
    ]


def test_search_users_by_email_returns_multiple_users(client):
    response = client.get("/users/search", params={"email": "@example"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]


def test_search_users_by_email_returns_empty_list(client):
    response = client.get("/users/search", params={"email": "missing"})

    assert response.status_code == 200
    assert response.json() == []


def test_search_users_by_email_rejects_one_character_keyword(client):
    response = client.get("/users/search", params={"email": "a"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Search keyword must be at least 2 characters"


def test_search_users_by_email_accepts_two_character_keyword(client):
    response = client.get("/users/search", params={"email": "bo"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == 204

    response = client.get("/users/1")
    assert response.status_code == 404
