from app.store import get_users


class EmailAlreadyExistsError(Exception):
    """Raised when a user is created with an email that is already registered."""


def normalize_email(email: str) -> str:
    """Return the comparison key of an email address.

    Email uniqueness is case-insensitive, so comparisons are made on the
    normalized value. The value stored on the user is left untouched.
    """
    return email.strip().lower()


def list_users() -> list[dict]:
    return list(get_users().values())


def get_user(user_id: int) -> dict | None:
    return get_users().get(user_id)


def find_user_by_email(email: str) -> dict | None:
    key = normalize_email(email)

    for user in get_users().values():
        if normalize_email(user["email"]) == key:
            return user

    return None


def next_user_id() -> int:
    users = get_users()

    # IDs are derived from the highest ID currently stored rather than from
    # the number of stored users, so a deletion can never make the next ID
    # collide with (and overwrite) an existing user.
    if not users:
        return 1

    return max(users) + 1


def create_user(name: str, email: str) -> dict:
    users = get_users()

    if find_user_by_email(email) is not None:
        raise EmailAlreadyExistsError(email)

    new_id = next_user_id()

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
