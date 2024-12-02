from typing import Any
from datetime import datetime
from logging.handlers import RotatingFileHandler
from threading import Lock
from os.path import isfile
import logging
import csv
import io


class CsvLogger:
    def __init__(self, filename: str, headers: str) -> None:
        self.filename = filename
        self.lock = Lock()
        self.output_io = io.StringIO()
        self.writer_io = csv.writer(
            self.output_io, delimiter=";", quoting=csv.QUOTE_ALL
        )
        self.wheaders(headers)

    def wheaders(self, headers: str) -> None:
        if not isfile(self.filename):
            with open(self.filename, "a") as file:
                file.write(headers + "\n")

    def acquire(self) -> None:
        self.lock.acquire()

    def release(self) -> None:
        self.lock.release()

    def info(self, record: Any) -> None:
        self.acquire()
        with open(self.filename, "a") as file:
            if isinstance(record, list):
                list(map(lambda x: file.write(self.format(x) + "\n"), record))
            else:
                file.write(self.format(record) + "\n")
        self.release()

    def format(self, record: Any) -> str:
        date = datetime.today().strftime("%Y-%m-%d , %H:%M:%S")
        if isinstance(record, dict):
            self.writer_io.writerow([date] + list(record.values()))
        elif isinstance(record, list):
            self.writer_io.writerow([date] + record)
        data = self.output_io.getvalue()
        self.output_io.truncate(0)
        self.output_io.seek(0)
        return data.strip()


def get_csv_logger(log_filename: str, headers: str) -> CsvLogger:
    return CsvLogger(log_filename, headers)


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
