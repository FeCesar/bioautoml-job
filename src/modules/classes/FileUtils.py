import zipfile
import glob

from ..services.logger_service import get_logger

logger = get_logger('FileUtils')
DEFAULT_ZIP_NAME = 'results.zip'


class FileUtils:

    @classmethod
    def compress_folder(cls, folder_path):
        logger.info(f'start to compress={folder_path}')
        zip_path_folder = folder_path + DEFAULT_ZIP_NAME

        with zipfile.ZipFile(zip_path_folder, 'w') as f:
            for file in glob.glob(folder_path):
                f.write(file)

        logger.info(f'finish to compress={folder_path} - created={zip_path_folder}')

        return zip_path_folder
