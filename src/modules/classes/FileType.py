from enum import Enum


class FileType(Enum):
    TRAIN = "TRAIN"
    LABEL_TRAIN = "LABEL_TRAIN"
    TEST = "TEST"
    LABEL_TEST = "LABEL_TEST"
    SEQUENCE = "SEQUENCE"
