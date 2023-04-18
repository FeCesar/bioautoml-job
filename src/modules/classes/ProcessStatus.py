from enum import Enum


class ProcessStatus(Enum):
    WAITING = "WAITING"
    PROCESSING = "PROCESSING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"
