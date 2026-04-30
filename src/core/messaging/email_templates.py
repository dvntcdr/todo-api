def welcome_email(username: str) -> str:
    return f'''
        <h2>Welcome to Todo App, {username}!</h2>
        <p>Your account has been created successfully.</p>
        <p>You can now log in and start managing your tasks and projects :)</p>
    '''
