from os import environ
import logging


def get_logger(name):
    log_level = environ.get("APP_LOGGER_LEVEL")
    log_formatter = "[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] [thread=%(thread)d] " \
                    "[%(levelname)s] [%(message)s]"

    logging.basicConfig(format=log_formatter, level=log_level)

    logger = logging.getLogger(name)

    return logger
