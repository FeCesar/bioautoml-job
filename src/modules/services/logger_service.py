from os import environ
from datetime import datetime
import logging


def get_logger(name):
    log_level = environ.get("APP_LOGGER_LEVEL")
    log_formatter = "[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] [thread=%(thread)d] " \
                    "[%(levelname)s] [%(message)s]"

    now = datetime.now()
    now = now.strftime("%m-%d-%YT%H:%M:%S")

    log_filename = f"./logs/app-{now}.log"

    logging.basicConfig(filename=log_filename, filemode='w', format=log_formatter, level=log_level)

    logger = logging.getLogger(name)

    return logger
