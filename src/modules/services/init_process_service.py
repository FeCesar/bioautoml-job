import base64
import json
import traceback
from types import SimpleNamespace
from os import environ

from ..services.logger_service import get_logger
from ..services.os_service import create_folder
from ..classes.RcloneService import RcloneService
from ..classes.ProcessType import ProcessTypes
from ..classes.FileType import FileType

logger = get_logger(__name__)

rclone_extract_files_folder_path = environ.get("APP_RCLONE_EXTRACT_FILES_FOLDER_PATH")
bioautoml_app_path = environ.get("APP_BIOAUTOML_PATH")
output_local_files = environ.get("APP_OUTPUT_FILES")
rclone = RcloneService()


def start(message):
    try:
        decoded_message = _decode(message)
        process = json.loads(decoded_message, object_hook=lambda d: SimpleNamespace(**d))
        prepare(process)
    except Exception as e:
        logger.error("Exception %s: %s" % (type(e), e))
        logger.debug(traceback.format_exc())


def prepare(process):
    _prepare_files(process)
    bash_command = _generate_bash_command(process)
    logger.info(f'created bash_command={bash_command}')


def _prepare_files(process):
    process_id = process.processModel.id
    process_files_remote_path = rclone.bucket + '/' + process_id + '/'
    process_files_local_path = _generate_files_path(process_id)
    process_files_local_output = _remove_double_bar(output_local_files + process.parametersEntity.output)

    create_folder(process_files_local_path)
    create_folder(process_files_local_output)
    rclone.copy(process_files_remote_path, process_files_local_path)


def _generate_files_path(process_id):
    return str(rclone_extract_files_folder_path + process_id + '/')


def _generate_bash_command(process):
    process_types = ProcessTypes[process.processModel.processType].value
    process_reference = process_types.get('reference')
    process_type = process_types.get('type')

    if process_type == 'AFEM_PARAMETERS':
        return _generate_afem_bash_command(process, process_reference)

    if process_type == 'METALEARNING_PARAMETERS':
        return _generate_metalearning_bash_command(process, process_reference)


def _generate_afem_bash_command(process, process_reference):
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

    output_path_files = _remove_double_bar(output_local_files + process.parametersEntity.output)
    estimations = process.parametersEntity.estimations
    cpu_numbers = process.parametersEntity.cpuNumbers

    bash_command = 'python '
    bash_command += f'{bioautoml_app_path}'
    bash_command += f'{process_reference} '
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


def _generate_metalearning_bash_command(process, process_reference):
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

    output_path_files = _remove_double_bar(output_local_files + process.parametersEntity.output)
    classifier = process.parametersEntity.classifiers
    normalization = process.parametersEntity.normalization
    imbalance = process.parametersEntity.imbalance
    tuning = process.parametersEntity.tuning
    cpu_numbers = process.parametersEntity.cpuNumbers

    bash_command = 'python '
    bash_command += f'{bioautoml_app_path}'
    bash_command += f'{process_reference} '
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


def _remove_double_bar(string):
    return string.replace('//', '/')


def _decode(process):
    return base64.b64decode(process)
