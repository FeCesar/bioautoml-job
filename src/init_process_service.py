import logging
import base64
import json
from types import SimpleNamespace

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(message):
    decoded_message = decode(message)
    process = json.loads(decoded_message, object_hook=lambda d: SimpleNamespace(**d))

    logger.info(process)
    logger.info(process.processModel)
    logger.info(process.parametersEntity)

    for file in process.files:
        logger.info(file)


def decode(process):
    return base64.b64decode(process)
