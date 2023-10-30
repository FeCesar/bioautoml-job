from os import environ
import logging
import json_log_formatter


def get_logger(name):
    log_level = environ.get("APP_LOGGER_LEVEL")

    formatter = json_log_formatter.VerboseJSONFormatter()
    json_handler = logging.FileHandler(filename='/app.json')
    json_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(json_handler)
    logger.setLevel(log_level)

    return logger
