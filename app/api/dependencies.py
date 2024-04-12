from fastapi import Header

from exceptions import AuthenticationError

# заглушка
user_token = "9e4328cad64f4e51aef1dbc6322db313"
admin_token = "admin_token"


def authenticate_user_token(token: str = Header(None)):
    if token != user_token:
        raise AuthenticationError("Отсутствует токен пользователя")


def authenticate_admin_token(token: str = Header(None)):
    if token != admin_token:
        raise AuthenticationError("Отсутствует токен админа")
