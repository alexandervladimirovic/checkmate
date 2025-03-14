from typing import NoReturn, Optional, Callable

from fastapi.exceptions import HTTPException

from .logger import setup_logger


log = setup_logger()


def handle_jwt_error(
    status_code: int,
    message: str,
    log_message: str,
    log_level: Callable[[str], None] = log.error,
    user_id: Optional[int] = None,
) -> NoReturn:
    """Handle JWT errors to avoid repeating logic.

    :param status_code(int): HTTP status errors (ex. 404, 501 and etc) that is passed to HTTPException in the status_code field.
    :param message(str): The error message that is passed to HTTPException in the detail field.
    :param log_message(str): This message will be different from what was passed in the message for clarity and debugging of the code.
    :param log_level(callable): A function used for logging (default=log.error).
    :param user_id(int): ID user (Optional). If the user_id is None, then logging will be performed without specifying the user_id.

    """
    if user_id:
        log_level(f"{log_message}, Пользователь ID: {user_id}")
    else:
        log_level(log_message)

    raise HTTPException(status_code=status_code, detail=[{"msg": message}])
