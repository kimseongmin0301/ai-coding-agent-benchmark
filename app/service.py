from app.store import get_users


def list_users() -> list[dict]:
    return list(get_users().values())


def get_user(user_id: int) -> dict | None:
    return get_users().get(user_id)


def create_user(name: str, email: str) -> dict:
    users = get_users()

    # NOTE:
    # The current ID generation logic is intentionally simplistic.
    # Task 002 requires the agent to inspect whether this is safe.
    new_id = len(users) + 1

    user = {
        "id": new_id,
        "name": name,
        "email": email,
    }

    users[new_id] = user
    return user


def delete_user(user_id: int) -> bool:
    users = get_users()
    if user_id not in users:
        return False

    del users[user_id]
    return True
