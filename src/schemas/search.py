from pydantic import BaseModel, Field

from src.schemas.project import ProjectResponse
from src.schemas.task import TaskResponse


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=100)
    limit: int = Field(10, ge=1, le=50)


class SearchResponse(BaseModel):
    tasks: list[TaskResponse]
    projects: list[ProjectResponse]
    total: int
