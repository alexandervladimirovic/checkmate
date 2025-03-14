from typing import Any
from datetime import datetime, timedelta

from authlib.jose import jwt
from authlib.jose.errors import InvalidTokenError, ExpiredTokenError

from .utils import handle_errors
from .exceptions import CreateJWTException, CreateRefreshTokenException
from ..logger import setup_logger
from ..mixins import utc
from ..settings import LIFETIME_ACCESS_TOKEN_IN_MINUTE, LIFETIME_REFRESH_TOKEN_IN_DAYS

log = setup_logger()

# to-do: repeat logic exception in create_jwt and create_refresh_token fix.
# to-do: exception in create_jwt and create_refresh_token fix.

def create_jwt(payload: dict[str, Any], private_key: str) -> str:
    """Create access token using library authlib with RS256 algorithm.

    :param payload(dict): Data to include in JWT payload (user info).
    :param private_key(str): Private key to sign JWT.

    :return(str): Access Token

    """
    try:
        headers = {"alg": "RS256"}
        payload["exp"] = datetime.now(utc) + timedelta(
            minutes=LIFETIME_ACCESS_TOKEN_IN_MINUTE
        )
        access_token = jwt.encode(headers, payload, private_key)
        return access_token
    except InvalidTokenError:
        handle_errors(
            CreateJWTException,
            "Недействительный токен",
            "Структура токена некорректна или несоответствует ожидаемому формату.",
        )
    except ExpiredTokenError:
        handle_errors(
            CreateJWTException,
            "Access токен истек",
            "Время токена истекло, проверьте настройку payload['exp'] в функции create_jwt.",
        )
    except Exception as exc:
        handle_errors(
            CreateJWTException,
            "Непредвиденная ошибка",
            f"Возникла непредвиденная ошибка при создании access token: {exc}.",
            log.exception,
        )


def create_refresh_token(payload: dict[str, Any], private_key: str) -> str:
    """Create refresh token using library authlib with RS256 algorithm.

    :param payload(dict): Data to include in the JWT payload (user info).
    :privaty_key(str): Private key to sign the JWT.

    :return(str): Refresh token for updating access tokens.

    """
    try:
        headers = {"alg": "RS256"}
        payload["exp"] = datetime.now(utc) + timedelta(
            days=LIFETIME_REFRESH_TOKEN_IN_DAYS
        )
        refresh_token = jwt.encode(headers, payload, private_key)
        return refresh_token
    except InvalidTokenError:
        handle_errors(
            CreateRefreshTokenException,
            "Недействительный токен",
            "Структура токена некорректна или несоответствует ожидаемому формату.",
        )
    except ExpiredTokenError:
        handle_errors(
            CreateRefreshTokenException,
            "Refresh токен истек",
            "Время токена истекло, проверьте настройку payload['exp'] в функции create_refresh_token.",
        )
    except Exception as exc:
        handle_errors(
            CreateRefreshTokenException,
            "Непредвиденная ошибка",
            f"Возникла непредвиденная ошибка при создании refresh token: {exc}.",
            log.exception,
        )


def verify_jwt(token: str, public_key: str) -> dict:
    """Verify access token or refresh token.

    :param token(str): access token or refresh token.
    :param public_key(str): Public key to verify token signature.

    :return(dict): Decoded payload of token if valid, or None if invalid.

    """
    try:
        payload = jwt.decode(token, public_key)
        payload.validate()
        return payload
    except ...:
        ...
