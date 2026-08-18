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


def test_search_users_by_email_returns_matching_user(client):
    response = client.get("/users/search", params={"email": "alice"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Alice", "email": "alice@example.com"}
    ]


def test_search_users_by_email_is_case_insensitive(client):
    upper = client.get("/users/search", params={"email": "ALICE"})
    lower = client.get("/users/search", params={"email": "alice"})

    assert upper.status_code == 200
    assert upper.json() == lower.json()
    assert [user["id"] for user in upper.json()] == [1]


def test_search_users_by_email_returns_every_match(client):
    response = client.get("/users/search", params={"email": "@example"})

    assert response.status_code == 200
    assert [user["id"] for user in response.json()] == [1, 2]


def test_search_users_by_email_returns_empty_list_when_no_match(client):
    response = client.get("/users/search", params={"email": "nobody"})

    assert response.status_code == 200
    assert response.json() == []


def test_search_users_by_email_rejects_short_keyword(client):
    response = client.get("/users/search", params={"email": "a"})

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Search keyword must be at least 2 characters"
    )


def test_search_users_by_email_accepts_two_character_keyword(client):
    response = client.get("/users/search", params={"email": "al"})

    assert response.status_code == 200
    assert [user["id"] for user in response.json()] == [1]


def test_search_users_by_email_requires_the_email_parameter(client):
    response = client.get("/users/search")

    assert response.status_code == 422

    # The error must be about the missing "email" query parameter, not about
    # "/users/{user_id}" trying to parse "search" as an int.
    locations = [detail["loc"] for detail in response.json()["detail"]]
    assert ["query", "email"] in locations


def test_search_route_is_not_captured_by_the_user_id_route(client):
    # "/users/search" must not be parsed as "/users/{user_id}".
    # Without the declaration order fix this returns 422 (int_parsing).
    search = client.get("/users/search", params={"email": "alice"})
    assert search.status_code == 200

    # Any other non-numeric segment still resolves to /users/{user_id}.
    assert client.get("/users/abc").status_code == 422


def test_existing_user_endpoints_are_unchanged_by_search(client):
    assert client.get("/health").json() == {"status": "ok"}

    listed = client.get("/users")
    assert listed.status_code == 200
    assert len(listed.json()) == 2

    detail = client.get("/users/1")
    assert detail.status_code == 200
    assert detail.json() == {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
    }

    assert client.get("/users/999").status_code == 404
