from fastapi import FastAPI, HTTPException, status

from app.models import UserCreate, UserResponse
from app.service import (
    create_user,
    delete_user,
    get_user,
    list_users,
    search_users_by_email,
)

app = FastAPI(title="AI Coding Agent Benchmark API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/users", response_model=list[UserResponse])
def users() -> list[dict]:
    return list_users()


MIN_SEARCH_KEYWORD_LENGTH = 2


# NOTE:
# This route must stay declared BEFORE "/users/{user_id}".
# FastAPI matches routes in declaration order, so if "/users/{user_id}" came
# first it would capture "/users/search" and fail to parse "search" as an int.
@app.get("/users/search", response_model=list[UserResponse])
def search_users(email: str) -> list[dict]:
    if len(email) < MIN_SEARCH_KEYWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Search keyword must be at least "
                f"{MIN_SEARCH_KEYWORD_LENGTH} characters"
            ),
        )

    return search_users_by_email(email)


@app.get("/users/{user_id}", response_model=UserResponse)
def user(user_id: int) -> dict:
    result = get_user(user_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return result


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_user(payload: UserCreate) -> dict:
    return create_user(payload.name, payload.email)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int) -> None:
    deleted = delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
