import base64
import json
from types import SimpleNamespace
from os import environ
from sys import platform

from ..services.logger_service import get_logger
from ..services.os_service import create_folder
from ..classes.RcloneService import RcloneService

logger = get_logger(__name__)

rclone_extract_files_folder_path = environ.get("APP_RCLONE_EXTRACT_FILES_FOLDER_PATH")
rclone = RcloneService()


def start(message):
    decoded_message = _decode(message)
    process = json.loads(decoded_message, object_hook=lambda d: SimpleNamespace(**d))

    prepare(process)


def prepare(process):
    _prepare_files(process.processModel.id)


def _prepare_files(process_id):
    process_files_remote_path = rclone.bucket + '/' + process_id + '/'
    process_files_local_path = rclone_extract_files_folder_path + '/' + process_id + '/'
    is_win = False

    if 'win32' in platform:
        is_win = True

    create_folder(process_files_local_path, is_win)

    rclone.copy(process_files_remote_path, process_files_local_path, is_win)


def _decode(process):
    return base64.b64decode(process)
