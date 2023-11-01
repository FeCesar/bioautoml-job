import zipfile
import os
import pathlib

from ..services.logger_service import get_logger

logger = get_logger('FileUtils')
DEFAULT_ZIP_NAME = 'results.zip'
IGNORED_FILES = ['results.zip', 'output.log']


class FileUtils:

    @classmethod
    def compress_folder(cls, folder_path):
        logger.info(f'start to compress={folder_path}')
        folder = pathlib.Path(folder_path)
        owd = os.getcwd()
        os.chdir(folder)

        with zipfile.ZipFile(DEFAULT_ZIP_NAME, 'w') as z:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.name not in IGNORED_FILES:
                        z.write(os.path.join(root, file))
                for directory in dirs:
                    if file.name not in IGNORED_FILES:
                        z.write(os.path.join(root, directory))

        os.chdir(owd)

        zip_name = folder_path + DEFAULT_ZIP_NAME
        logger.info(f'finish to compress={folder_path} - created={zip_name}')

        return zip_name
