from os import environ

from docker import from_env

from ..services.logger_service import get_logger

logger = get_logger(__name__)


class RcloneService:

    def __init__(self):
        self.client = from_env()
        self.image = 'rclone/rclone:latest'
        self.detach = True
        self.rclone_config_path = environ.get("APP_RCLONE_CONFIG_PATH")
        self.config_file = self.rclone_config_path + ':/config/rclone/'
        self.bucket = 's3:bioautomlfolders'

    def copy(self, source_from, source_to, is_win):
        logger.info(f'copy files from={source_from} to={source_to}')

        if is_win:
            win_path = 'C:' + source_to
            volumes = [self.config_file, f'{win_path}:{source_to}']
        else:
            volumes = [self.config_file, f'{source_to}:{source_to}']

        self.client.containers.run(image=self.image, detach=self.detach, volumes=volumes,
                                   command=['copy', source_from, source_to])
