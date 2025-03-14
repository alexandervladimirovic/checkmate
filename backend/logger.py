import os
import sys

from loguru import Logger, logger


LOG_DIR = "logs"
MIN_LOGGER_LEVEL_FOR_CONSOLE_OUTPUT = "DEBUG"
MIN_LOGGER_LEVEL_FOR_FILE_OUTPUT = "INFO"
MIN_LOGGER_LEVEL_FOR_ERROR_FILE_OUTPUT = "ERROR"


if not os.path.exists(LOG_DIR):
    try:
        os.makedirs(LOG_DIR)
    except Exception as exc:
        raise exc from None


def setup_logger() -> Logger:
    """Setup logging for apps.
    
    This function removes all existing logging handlers and adds new ones:
        - Output logs to the console with a minimum 'DEBUG' level.
        - Output logs to a file with a minimum 'INFO' level and time rotation.
        - Output error logs to a separate file with a minimum 'ERROR' level and time rotation.

    Logs are rotated every day at midnight, old logs are stored for 7 days, compressed into zip archives.

    """

    # remove default setup logger
    logger.remove()

    # console output
    logger.add(
        sys.stdout,
        level=MIN_LOGGER_LEVEL_FOR_CONSOLE_OUTPUT,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

    # file output
    logger.add(
        os.path.join(LOG_DIR, "{time:YYYY-MM-DD}.log"),
        level=MIN_LOGGER_LEVEL_FOR_FILE_OUTPUT,
        rotation="00:00",
        retention="7 days",
        compression="zip",
    )

    # error file output
    logger.add(
        os.path.join(LOG_DIR, "error.log"),
        level=MIN_LOGGER_LEVEL_FOR_ERROR_FILE_OUTPUT,
        rotation="00:00",
        retention="7 days",
        compression="zip",
    )

    return logger
