from os import path, makedirs

from ..services.logger_service import get_logger


logger = get_logger(__name__)


def create_folder(source_path):
    if not path.exists(source_path):
        logger.info('create path=' + source_path)
        makedirs(source_path)