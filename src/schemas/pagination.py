from pydantic import BaseModel, Field

from src.core.config import settings


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(settings.PAGINATION_LIMIT, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PagedResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(cls, items: list[T], total: int, params: PaginationParams) -> PagedResponse[T]:
        total_pages=-(-total // params.limit)
        return cls(
            items=items,
            total=total,
            page=params.page,
            limit=params.limit,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_previous=params.page > 1
        )
