from datetime import datetime

from ..services.logger_service import get_logger


logger = get_logger(__name__)


def print_now():
    logger.info(datetime.now().__str__())


if __name__ == "__update_processes_production__":
    print_now()
