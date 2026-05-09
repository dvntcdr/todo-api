from pydantic import BaseModel, Field

from src.schemas.project import ProjectResponse
from src.schemas.task import TaskResponse
from src.schemas.user import UserResponse


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=100)
    limit: int = Field(10, ge=1, le=50)


class SearchResponse(BaseModel):
    tasks: list[TaskResponse]
    projects: list[ProjectResponse]
    users: list[UserResponse]
    total: int
