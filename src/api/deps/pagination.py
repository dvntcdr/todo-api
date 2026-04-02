from typing import Annotated

from fastapi import Depends

from src.schemas.pagination import PaginationParams

PaginationDep = Annotated[PaginationParams, Depends()]
