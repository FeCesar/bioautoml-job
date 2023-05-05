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

        with zipfile.ZipFile(DEFAULT_ZIP_NAME, 'w',  zipfile.ZIP_DEFLATED) as zip:
            for file in folder.iterdir():
                if file.name not in IGNORED_FILES:
                    zip.write(file)

        os.chdir(owd)

        zip_name = folder_path + DEFAULT_ZIP_NAME
        logger.info(f'finish to compress={folder_path} - created={zip_name}')

        return zip_name
