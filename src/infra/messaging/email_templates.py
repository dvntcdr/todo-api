from src.core.config import settings


def welcome_email(username: str) -> str:
    """
    Generate a welcome email template for the given username.

    Args:
        username (str): The username of the recipient.

    Returns:
        str: The HTML content of the welcome email.
    """
    return f'''
        <h2>Welcome to Todo App, {username}!</h2>
        <p>Your account has been created successfully.</p>
        <p>You can now log in and start managing your tasks and projects :)</p>
    '''


def due_date_reminder_email(username: str, data: list[dict]) -> str:
    """
    Generate a due date reminder email template for the given username and task data.

    Args:
        username (str): The username of the recipient.
        data (list[dict]): A list of task dictionaries with 'title' and 'due_date' keys.

    Returns:
        str: The HTML content of the due date reminder email.
    """
    task_list = ''.join(
        [
            f'''
                <li>
                    <strong>{task['title']}</strong>
                    - due {task['due_date']}
                </li>
            '''
            for task in data
        ]
    )

    return f'''
        <h2>Hi {username}, you have tasks due tommorow!</h2>
        <ul>{task_list}</ul>
        <p>Stay on top of your work!</p>
    '''


def password_reset_email(username: str, reset_token: str) -> str:
    """
    Generate a password reset email template for the given username and reset token.

    Args:
        username (str): The username of the recipient.
        reset_token (str): The password reset token to include in the email.

    Returns:
        str: The HTML content of the password reset email.
    """
    return f'''
        <h2>Hi {username}, you requested a password reset.</h2>
        <p>Use the token below to reset your password. It expires in {settings.RESET_TOKEN_EXPIRE_MINUTES} minutes and can only be used once!</p>
        <hr>
        <p>{reset_token}</p>
        <hr>
        <p>If you did not request this, you can safely ignore this email.</p>
    '''
