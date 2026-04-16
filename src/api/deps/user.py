from typing import Annotated

from fastapi import Depends

from src.api.deps.repos import UserRepoDep
from src.services.user import UserService


def get_user_service(repo: UserRepoDep) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
