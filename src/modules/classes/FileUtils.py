import zipfile
import glob

from ..services.logger_service import get_logger

logger = get_logger('FileUtils')
DEFAULT_ZIP_NAME = 'results.zip'


class FileUtils:

    @classmethod
    def compress_folder(cls, folder_path):
        logger.info(f'start to compress={folder_path}')

        with zipfile.ZipFile(DEFAULT_ZIP_NAME, 'w') as f:
            for file in glob.glob(folder_path):
                f.write(file)

        zip_name = folder_path + DEFAULT_ZIP_NAME
        logger.info(f'finish to compress={folder_path} - created={zip_name}')

        return zip_name
