from typing import Any
from uuid import UUID


def user_key_by_id(id: UUID) -> str:
    return f'user:id:{str(id)}'


def user_key_by_username(username: str) -> str:
    return f'user:username:{username}'


def get_cache_key(prefix: str, identifier: Any) -> str:
    return f'{prefix}:{str(identifier)}'


def reset_token_key(token_hash: str) -> str:
    return f'reset_token:{token_hash}'
