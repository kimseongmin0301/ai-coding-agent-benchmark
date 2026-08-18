from app.store import get_users


class DuplicateEmailError(ValueError):
    pass


def list_users() -> list[dict]:
    return list(get_users().values())


def get_user(user_id: int) -> dict | None:
    return get_users().get(user_id)


def create_user(name: str, email: str) -> dict:
    users = get_users()

    normalized_email = email.casefold()
    if any(user["email"].casefold() == normalized_email for user in users.values()):
        raise DuplicateEmailError("Email already exists")

    new_id = max(users.keys(), default=0) + 1

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
