from os import environ
from time import sleep
import json

from docker import from_env

from ..services.logger_service import get_logger

logger = get_logger(__name__)


def _container_is_exited(status):
    return not status == 'exited'


def _get_container_status(container_attrs):
    json_container_attrs = json.dumps(container_attrs)
    json_load_container_attrs = json.loads(json_container_attrs)

    return json_load_container_attrs['Status']


class RcloneService:

    def __init__(self):
        self.client = from_env()
        self.image = 'rclone/rclone:latest'
        self.detach = True
        self.rclone_config_path = environ.get("APP_RCLONE_CONFIG_PATH")
        self.config_file = self.rclone_config_path + ':/config/rclone/'
        self.bucket = 's3:bioautomlfolders'

    def copy(self, source_from, source_to):
        logger.info(f'copy files from={source_from} to={source_to}')

        if self.bucket in source_to:
            volumes = [self.config_file]
        else:
            volumes = [self.config_file, f'{source_to}:{source_to}']

        container = self.client.containers.run(image=self.image, detach=self.detach, volumes=volumes,
                                               command=['copy', source_from, source_to])

        is_not_exited = True

        while is_not_exited:
            container_updated = self.client.containers.get(container.id)
            container_attrs = container_updated.attrs['State']
            container_status = _get_container_status(container_attrs)
            is_not_exited = _container_is_exited(container_status)
            sleep(2)

        container.remove()
