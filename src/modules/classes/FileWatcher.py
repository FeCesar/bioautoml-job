import os
from time import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ..services.logger_service import get_logger
from ..classes.RcloneService import RcloneService
from ..classes.FileUtils import FileUtils


logger = get_logger("FileWatcher")


class FileWatcher(FileSystemEventHandler):

    def __init__(self, src_path, process_id):
        self.__src_path = src_path
        self.__process_id = process_id
        self.__observer = Observer()
        self.__rclone = RcloneService()

    def on_created(self, event):
        logger.info(f'event-path={event.src_path} & event-type={event.event_type}')

    def on_modified(self, event):
        logger.info(f'event-path={event.src_path} & event-type={event.event_type}')

    def watch(self):
        retries = 3
        exception = None
        file_size = 0

        while retries > 0:
            try:
                file_size = os.path.getsize(self.__src_path + 'output.log')
                retries = -1
            except Exception as e:
                FileWatcher.__pause(7)
                exception = e
                retries -= 1

        if retries == -1:
            self.__observer.schedule(self, path=self.__src_path, recursive=True)
            self.__observer.start()
            logger.info(f'monitoring start from path={self.__src_path}')

            while file_size <= 1:
                FileWatcher.__pause(60)
                file_size = os.path.getsize(self.__src_path + 'output.log')

            self.__observer.stop()
            self.__observer.join()
            logger.info(f'monitoring finished from path={self.__src_path}')

            zip_name = FileUtils.compress_folder(self.__src_path)
            self.__rclone.copy(zip_name, self.__rclone.bucket + '/' + self.__process_id)

        else:
            raise exception

    @classmethod
    def __pause(cls, secs):
        init_time = time()
        while time() < init_time + secs:
            pass
