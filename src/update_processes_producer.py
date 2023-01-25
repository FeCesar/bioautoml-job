from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def print_now():
    logger.info(datetime.now().__str__())


if __name__ == "__update_processes_production__":
    print_now()
