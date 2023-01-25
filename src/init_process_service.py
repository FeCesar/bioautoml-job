import logging
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(process):
    print(decode(process))


def decode(process):
    return base64.b64decode(process)
