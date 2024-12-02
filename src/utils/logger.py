from logging.handlers import RotatingFileHandler
import logging


FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")


def __get_file_handler(filename: str, level: int) -> logging.Handler:
    file_handler = RotatingFileHandler(
        "./logs/" + filename, mode="a", maxBytes=1024 * 1024 * 500, backupCount=10
    )
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(level)

    return file_handler


def __set_logging_level(environment: str) -> int:
    if environment == "production":
        return logging.INFO
    return logging.DEBUG


def get_logger(logger_name: str) -> logging.Logger:
    from src.utils import settings

    logger = logging.getLogger(logger_name)
    logger.setLevel(__set_logging_level(settings.ENVIRONMENT))
    logger.addHandler(__get_file_handler(settings.APP_LOGGER_FILE, logging.INFO))
    logger.addHandler(
        __get_file_handler(settings.EXCEPTIONS_LOGGER_FILE, logging.ERROR)
    )
    logger.propagate = False

    return logger


class Logger:
    def __init__(self) -> None:
        # self.setup_logger()
        # self.database_logger = get_logger("database")
        # self.eventbus_logger = get_logger("eventbus")
        self.api_logger = get_logger("api")
        self.background_logger = get_logger("background")

    # def setup_logger(self) -> None:
    #    logging.basicConfig(level=logging.INFO)


logger = Logger()
