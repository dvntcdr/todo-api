from uuid import UUID

from src.core.config import settings
from src.core.exceptions import (
    AlreadyExistsException,
    ForbiddenException,
    InvalidCredentialsException,
    InvalidOperationException,
)
from src.infra.caching.cache_keys import get_cache_key
from src.infra.caching.cache_manager import CacheManager
from src.infra.caching.cache_service import CacheService
from src.infra.security.auth import (
    create_verification_token,
    hash_verification_token,
    verify_password,
)
from src.models.user import User
from src.repos.user import UserRepository
from src.schemas.pagination import PagedResponse, PaginationParams
from src.schemas.user import (
    ChangeEmailRequest,
    ChangeUsernameRequest,
    UserResponse,
)
from src.worker.tasks import send_email_change_verification


class UserService:
    """
    Service layer for managing users.

    Attributes:
        repo (UserRepository): Repository for user data access.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        cache: CacheService
    ) -> None:
        self.user_repo = user_repo
        self.user_cache = CacheManager(cache, User)
        self.cache = cache

    async def get_all(self, pg_params: PaginationParams) -> PagedResponse[UserResponse]:
        """
        Retrieve list of all users.  # TODO: update
        """

        items, total = await self.user_repo.get_all()

        return PagedResponse.create(items, total, pg_params)

    async def get_by_id(self, user_id: UUID) -> User:
        """
        Retrieve a single user by ID.
        """

        return await self.user_cache.get_or_fetch(
            get_cache_key('user:id', user_id),
            lambda: self.user_repo.get_by_id(user_id),
            use_cache=True
        )

    async def change_username(self, user: User, data: ChangeUsernameRequest) -> User:
        """
        Change the username of an existing user.
        """

        if not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsException()

        if data.new_username == user.username:
            raise InvalidOperationException('New username cannot be the same as the current username')

        existing = await self.user_repo.get_by_username(data.new_username)

        if existing is not None:
            raise AlreadyExistsException('Username is already taken')

        await self.user_cache.invalidate(get_cache_key('user:id', user.id))
        await self.user_cache.invalidate(get_cache_key('user:username', user.username))

        return await self.user_repo.update(user, {'username': data.new_username})

    async def initiate_change_email(self, user: User, data: ChangeEmailRequest) -> None:
        """
        Initiate email change flow for the current user.
        """

        if data.new_email == user.email:
            raise InvalidOperationException('New email cannot be the same as the current email')

        existing = await self.user_repo.get_by_email(email=data.new_email)

        if existing is not None:
            raise AlreadyExistsException('Email is already registered')

        raw_token, hashed_token = create_verification_token()
        key = get_cache_key('email_change_token', hashed_token)

        await self.cache.set(
            key,
            {
                'user_id': str(user.id),
                'new_email': data.new_email,
            },
            ttl=settings.VERIFICATION_TOKEN_EXPIRE_MINUTES * 60
        )

        send_email_change_verification.delay(user.username, data.new_email, raw_token)  # type: ignore

    async def confirm_email_change(self, user: User, token: str) -> User:
        """
        Verify a user's new email address using a verification token.
        """

        hashed_token = hash_verification_token(token)
        key = get_cache_key('email_change_token', hashed_token)

        payload = await self.cache.get(key)

        if payload is None:
            raise InvalidCredentialsException('Verification token is invalid or expired')

        if payload['user_id'] != str(user.id):
            raise ForbiddenException()

        existing = await self.user_repo.get_by_email(payload['new_email'])

        if existing is not None:
            raise AlreadyExistsException('Email is already registered')

        updated = await self.user_repo.update(user, {'email': payload['new_email']})

        await self.cache.invalidate(key)
        await self.user_cache.invalidate(get_cache_key('user:id', user.id))
        await self.user_cache.invalidate(get_cache_key('user:username', user.username))

        return updated
