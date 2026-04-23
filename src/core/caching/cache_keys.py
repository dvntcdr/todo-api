from uuid import UUID


def user_key_by_id(id: UUID) -> str:
    return f'user:id:{str(id)}'


def user_key_by_username(username: str) -> str:
    return f'user:username:{username}'


def task_key_by_id(id: UUID) -> str:
    return f'task:id:{str(id)}'
