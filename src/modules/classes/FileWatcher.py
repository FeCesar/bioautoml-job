import os
from time import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ..services.logger_service import get_logger
from ..classes.RcloneService import RcloneService


logger = get_logger("FileWatcher")


class FileWatcher(FileSystemEventHandler):

    def __init__(self, src_path, process_id):
        self.__src_path = src_path
        self.__process_id = process_id
        self.__observer = Observer()
        self.__rclone = RcloneService()

    def on_created(self, event):
        logger.info(f'event-path={event.src_path} & event-type={event.event_type}')
        self.__rclone.copy(event.src_path, self.__rclone.bucket + '/' + self.__process_id + '/results/')

    def on_modified(self, event):
        logger.info(f'event-path={event.src_path} & event-type={event.event_type}')
        self.__rclone.copy(event.src_path, self.__rclone.bucket + '/' + self.__process_id + '/results/')

    def watch(self):
        file_size = os.path.getsize(self.__src_path + 'output.log')
        self.__observer.schedule(self, path=self.__src_path, recursive=True)
        self.__observer.start()
        logger.info(f'monitoring start from path={self.__src_path}')

        while file_size <= 1:
            FileWatcher.__pause(60)
            file_size = os.path.getsize(self.__src_path + 'output.log')

        self.__observer.stop()
        self.__observer.join()
        logger.info(f'monitoring finished from path={self.__src_path}')

    @classmethod
    def __pause(cls, secs):
        init_time = time()
        while time() < init_time + secs:
            pass