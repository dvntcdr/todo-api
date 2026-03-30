from typing import Annotated

from fastapi import Depends

from src.api.deps.user import UserRepoDep
from src.services.auth import AuthService


def get_auth_service(user_repo: UserRepoDep) -> AuthService:
    return AuthService(user_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
