from typing import NoReturn, Callable

from logger import setup_logger


log = setup_logger()


def handle_errors(
    exception: Exception,
    message: str,
    log_message: str,
    log_level: Callable[[str], None] = log.error,
) -> NoReturn:
    """Function for raise PasswordHashingException and write message in log.

    :param message(str): Short message for information raises.
    :param log_message(str): Detail message for log file.
    :param log_level(callable): Level log(default=log.error).
    """
    log_level(log_message)
    raise exception(message)
