from unittest.mock import AsyncMock

import pytest

from src.infra.caching.cache_service import CacheService
from src.services.auth import AuthService
from src.services.membership import ProjectMemberService
from src.services.project import ProjectService
from src.services.task import TaskService
from src.services.user import UserService


@pytest.fixture
def cache_service() -> AsyncMock:
    service = AsyncMock(spec=CacheService)
    service.get.return_value = None
    service.get_or_fetch = AsyncMock(side_effect=lambda key, fetch, **kw: fetch())
    service.set = AsyncMock()
    service.invalidate = AsyncMock()
    return service


@pytest.fixture
def auth_service(user_repo, token_repo, cache_service) -> AuthService:
    return AuthService(user_repo, token_repo, cache_service)


@pytest.fixture
def user_service(user_repo) -> UserService:
    return UserService(user_repo)


@pytest.fixture
def task_service(task_repo, project_repo, member_repo, cache_service) -> TaskService:
    return TaskService(task_repo, project_repo, member_repo, cache_service)


@pytest.fixture
def project_service(project_repo, member_repo, cache_service) -> ProjectService:
    return ProjectService(project_repo, member_repo, cache_service)


@pytest.fixture
def member_service(member_repo, project_repo, user_repo, cache_service) -> ProjectMemberService:
    return ProjectMemberService(member_repo, project_repo, user_repo, cache_service)
