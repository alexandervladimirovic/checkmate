from typing import NoReturn

from argon2.exceptions import HashingError, InvalidHashError, VerifyMismatchError

from .utils import handle_errors
from .exceptions import PasswordHashingException, ValidatePasswordException
from logger import setup_logger
from settings import ph

log = setup_logger()


class PasswordServices:
    def hash_password(self, password: str) -> str:
        """Hashed password using Argin2 algorithm.

        :param password(str): Raw password entered user.
        :return(str): Hashed password.

        """

        if not isinstance(password, str):
            handle_errors(
                PasswordHashingException,
                "Неверный тип данных",
                "Для хэширования пароля нужно передать его в виде строки.",
            )

        try:
            self.validate_password(password)
            return ph.hash(password)
        except HashingError as exc:
            handle_errors(
                PasswordHashingException,
                "Ошибка при хешировании пароля",
                f"Возникла ошибка при хешировании пароля: {exc}.",
            )
        except InvalidHashError:
            handle_errors(
                PasswordHashingException,
                "Хэш не валиден",
                "Хэш не является валидным или не соответствует формату, ожидаемому алгоримом Argon2.",
            )
        except MemoryError:
            handle_errors(
                PasswordHashingException,
                "Ошибка памяти",
                "Операция хэширования требует слишком много памяти. Настройте параметр 'memory_cost' в Argon2.",
            )
        except Exception as exc:
            handle_errors(
                PasswordHashingException,
                "Непредвиденная ошибка",
                f"Возникла неожиданная ошибка при хэшировании пароля: {exc}.",
                log.exception,
            )

    def verify_password(self, password_hash: str, password: str) -> bool:
        if not self._validate_non_empty(password_hash, password):
            return False

        try:
            ph.verify(password_hash, password)
        except VerifyMismatchError:
            log.debug("Пароли не совпадают.")
            return False
        except InvalidHashError:
            log.debug("Невалидный хэш при проверке пароля.")
            return False
        except Exception as exc:
            log.debug(f"Возникла неожиданная ошибка при проверке пароля: {exc}.")
            return False
        return True

    def validate_password(self, password: str) -> NoReturn:
        if not password or len(password) < 8:
            handle_errors(
                ValidatePasswordException,
                "Длина меньше 8 символов",
                "Длина пароля должна составлять не меньше 8 символов.",
            )
        if " " in password:
            handle_errors(
                ValidatePasswordException,
                "Пароль содержит пробел",
                "Пароль не должен содержать в себе пробел.",
            )
        if not any(char.isdigit() for char in password):
            handle_errors(
                ValidatePasswordException,
                "Пароль не содержит цифру",
                "Пароль должен содержать хотя бы одну цифру.",
            )
        if not (
            any(char.isupper() for char in password)
            and any(char.islower() for char in password)
        ):
            handle_errors(
                ValidatePasswordException,
                "Пароль не содержит букву в верхнем и нижнем регистре",
                "Пароль должен содержать букву в верхнем и нижнем регистре.",
            )

    def _validate_non_empty(self, *args) -> bool:
        for arg in args:
            if not arg:
                log.debug("Не был передан один из обязательных параметров.")
                return False
            return True
