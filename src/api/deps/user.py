from typing import Annotated

from fastapi import Depends

from src.api.deps.session import SessionDep
from src.repos.user import UserRepository


def get_user_repo(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]
