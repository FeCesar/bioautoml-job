from watchdog.events import FileSystemEventHandler

from ..classes.RcloneService import RcloneService


class FileCreateHandler(FileSystemEventHandler):
    def __init__(self, process_files_remote_path):
        self.process_files_remote_path = process_files_remote_path

    def on_created(self, event):
        print("Created: " + event.src_path)
        RcloneService.copy(event.src_path, self.process_files_remote_path)
