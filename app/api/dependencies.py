from fastapi import Header

from app.exceptions import AuthenticationError

# заглушка
user_token = "user_token"
admin_token = "admin_token"


def authenticate_user_token(token: str = Header(None)):
    if token != user_token:
        raise AuthenticationError("Отсутствует токен пользователя")



def authenticate_admin_token(token: str = Header(None)):
    if token != admin_token:
        raise AuthenticationError("Отсутствует токен админа")
