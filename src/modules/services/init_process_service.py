import base64
import json
from types import SimpleNamespace
from os import environ
from sys import platform

from ..services.logger_service import get_logger
from ..services.os_service import create_folder
from ..classes.RcloneService import RcloneService
from ..classes.ProcessType import ProcessTypes
from ..classes.FileType import FileType

logger = get_logger(__name__)

rclone_extract_files_folder_path = environ.get("APP_RCLONE_EXTRACT_FILES_FOLDER_PATH")
bioautoml_app_path = environ.get("APP_BIOAUTOML_PATH")
rclone = RcloneService()


def start(message):
    decoded_message = _decode(message)
    process = json.loads(decoded_message, object_hook=lambda d: SimpleNamespace(**d))

    prepare(process)


def prepare(process):
    _prepare_files(process.processModel.id)

    bash_command = _generate_bash_command(process)
    logger.info(f'created bash_command={bash_command}')


def _prepare_files(process_id):
    process_files_remote_path = rclone.bucket + '/' + process_id + '/'
    process_files_local_path = _generate_files_path(process_id)
    is_win = False

    if 'win32' in platform:
        is_win = True

    create_folder(process_files_local_path, is_win)

    rclone.copy(process_files_remote_path, process_files_local_path, is_win)


def _generate_files_path(process_id):
    return str(rclone_extract_files_folder_path + '/' + process_id + '/')


def _generate_bash_command(process):
    parameter_type = ProcessTypes[process.processModel.processType]

    if parameter_type.value == 'AFEM_PARAMETERS':
        return _generate_afem_bash_command(process)

    if parameter_type.value == 'METALEARNING_PARAMETERS':
        return _generate_metalearning_bash_command(process)


def _generate_afem_bash_command(process):
    train_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.TRAIN.value, process.files))
    )
    label_train_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.LABEL_TRAIN.value, process.files))
    )
    test_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.TEST.value, process.files))
    )
    label_test_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.LABEL_TEST.value, process.files))
    )

    output_path_files = process.parametersEntity.output
    estimations = process.parametersEntity.estimations
    cpu_numbers = process.parametersEntity.cpuNumbers

    bash_command = 'python '
    bash_command += f'{bioautoml_app_path}/BioAutoML-feature.py '
    bash_command += f'-fasta_train {train_files}'
    bash_command += f'-fasta_label_train {label_train_files}'
    bash_command += f'-fasta_test {test_files}'
    bash_command += f'-fasta_label_test {label_test_files}'
    bash_command += f'-estimations {estimations} '
    bash_command += f'-n_cpu {cpu_numbers} '
    bash_command += f'-output {output_path_files}'

    return str(bash_command)


def _get_files_path(files):
    file_paths = ''

    for file in files:
        file_paths += _generate_files_path(file.processId)
        file_paths += file.fileName
        file_paths += ' '

    return file_paths


def _generate_metalearning_bash_command(process):
    train_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.TRAIN.value, process.files))
    )
    label_train_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.LABEL_TRAIN.value, process.files))
    )
    test_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.TEST.value, process.files))
    )
    label_test_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.LABEL_TEST.value, process.files))
    )
    sequence_files = _get_files_path(
        list(filter(lambda file: file.fileType == FileType.SEQUENCE.value, process.files))
    )

    output_path_files = process.parametersEntity.output
    classifier = process.parametersEntity.classifiers
    normalization = process.parametersEntity.normalization
    imbalance = process.parametersEntity.imbalance
    tuning = process.parametersEntity.tuning
    cpu_numbers = process.parametersEntity.cpuNumbers

    bash_command = 'python '
    bash_command += f'{bioautoml_app_path}/BioAutoML-feature.py '
    bash_command += f'-train {train_files}'
    bash_command += f'-train_label {label_train_files}'
    bash_command += f'-test {test_files}'
    bash_command += f'-test_label {label_test_files}'
    bash_command += f'-test_nameseq {sequence_files}'
    bash_command += f'-classifier {classifier} '
    bash_command += f'-nf {normalization} '
    bash_command += f'-n_cpu {cpu_numbers} '
    bash_command += f'-imbalance {imbalance} '
    bash_command += f'-tuning {tuning} '
    bash_command += f'-output {output_path_files}'

    return str(bash_command)


def _decode(process):
    return base64.b64decode(process)
