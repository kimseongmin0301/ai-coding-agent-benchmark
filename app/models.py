from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=3, max_length=120)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
