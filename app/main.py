from fastapi import FastAPI, HTTPException, status

from app.models import UserCreate, UserResponse
from app.service import (
    DuplicateEmailError,
    create_user,
    delete_user,
    get_user,
    list_users,
)

app = FastAPI(title="AI Coding Agent Benchmark API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/users", response_model=list[UserResponse])
def users() -> list[dict]:
    return list_users()


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
    try:
        return create_user(payload.name, payload.email)
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int) -> None:
    deleted = delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
