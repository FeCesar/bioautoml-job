import base64
import json
import traceback
from types import SimpleNamespace
from os import environ
from os import system

from ..producers.error_producer import send_error
from ..producers.update_processes_producer import update_status
from ..services.logger_service import get_logger
from ..services.os_service import create_folder
from ..classes.RcloneService import RcloneService
from ..classes.ProcessStatus import ProcessStatus
from ..classes.ProcessType import ProcessTypes
from ..classes.FileType import FileType
from ..classes.LabelType import LabelType
from ..classes.FileWatcher import FileWatcher
from ..classes.ThreadPoolService import ThreadPoolService

logger = get_logger(__name__)

rclone_extract_files_folder_path = environ.get("APP_RCLONE_EXTRACT_FILES_FOLDER_PATH")
bioautoml_app_path = environ.get("APP_BIOAUTOML_PATH")
output_local_files = environ.get("APP_OUTPUT_FILES")
miniconda_app_path = environ.get("APP_MINICONDA_PATH")
rclone = RcloneService()
amount_workers = int(environ.get("APP_WORKERS"))
thread_poll = ThreadPoolService(amount_workers)


def start(message):
    decoded_message = __decode(message)
    process = json.loads(decoded_message, object_hook=lambda d: SimpleNamespace(**d))
    update_status(ProcessStatus.PROCESSING.value, process.processModel.id)

    try:
        bash_command = __prepare(process)

        thread = thread_poll.get_worker()
        thread.submit(__run, bash_command, process)

        __observer_results(process)
        update_status(ProcessStatus.FINISHED.value, process.processModel.id)
    except Exception as e:
        logger.error("Exception %s: %s" % (type(e), e))
        logger.debug(traceback.format_exc())
        send_error(e, process.processModel.id)
        update_status(ProcessStatus.ERROR.value, process.processModel.id)


def __observer_results(process):
    path = __remove_double_bar(output_local_files + process.parametersEntity.output)
    watcher = FileWatcher(path, process.processModel.id)
    watcher.watch()


def __run(bash_command, process):
    process_files_local_output = __remove_double_bar(output_local_files + process.parametersEntity.output)
    all_bash_command = __complement_bash_command(bash_command, process_files_local_output)
    system(all_bash_command)


def __complement_bash_command(bash_command, process_files_local_output):
    bash = f'cd {bioautoml_app_path} && '
    bash += 'git pull && '
    bash += 'git submodule init && git submodule update && '
    bash += f'{miniconda_app_path}conda run -n bioautoml python {bash_command} >> {process_files_local_output}/output.log'

    logger.info(f'all bash command={__remove_double_bar(bash)}')

    return __remove_double_bar(bash)


def __prepare(process):
    __prepare_files(process)
    bash_command = __generate_bash_command(process)
    logger.info(f'created bash_command={bash_command}')

    return bash_command


def __prepare_files(process):
    process_id = process.processModel.id
    process_files_remote_path = rclone.bucket + '/' + process_id + '/'
    process_files_local_path = __generate_files_path(process_id)
    process_files_local_output = __remove_double_bar(output_local_files + process.parametersEntity.output)

    create_folder(process_files_local_path)
    create_folder(process_files_local_output)
    rclone.copy(process_files_remote_path, process_files_local_path)


def __generate_files_path(process_id):
    return str(rclone_extract_files_folder_path + process_id + '/')


def __generate_bash_command(process):
    process_types = ProcessTypes[process.processModel.processType].value
    process_reference = process_types.get('reference')
    process_type = process_types.get('type')

    if process_type == 'AFEM_PARAMETERS':
        return __generate_afem_bash_command(process, process_reference)

    if process_type == 'METALEARNING_PARAMETERS':
        return __generate_metalearning_bash_command(process, process_reference)


def __generate_afem_bash_command(process, process_reference):
    train_files = __get_files_path(
        list(filter(lambda file: file.fileType == FileType.TRAIN.value, process.files))
    )
    labels_train = __get_string_from_list(
        list(filter(lambda label: label.labelType == LabelType.TRAIN.value, process.labels))
    )
    test_files = __get_files_path(
        list(filter(lambda file: file.fileType == FileType.TEST.value, process.files))
    )
    labels_test = __get_string_from_list(
        list(filter(lambda label: label.labelType == LabelType.TEST.value, process.labels))
    )

    output_path_files = __remove_double_bar(output_local_files + process.parametersEntity.output)
    estimations = process.parametersEntity.estimations
    cpu_numbers = process.parametersEntity.cpuNumbers

    bash_command = f'{process_reference} '
    bash_command += f'-fasta_train {train_files}'
    bash_command += f'-fasta_label_train {labels_train}'

    if test_files != '':
        bash_command += f'-fasta_test {test_files}'
        bash_command += f'-fasta_label_test {labels_test}'

    bash_command += f'-estimations {estimations} '
    bash_command += f'-n_cpu {cpu_numbers} '
    bash_command += f'-output {output_path_files[:-1]}'

    return str(bash_command)


def __get_string_from_list(labels):
    text = ''

    for label in labels:
        text += f'{label.value} '

    return text


def __get_files_path(files):
    file_paths = ''

    for file in files:
        file_paths += __generate_files_path(file.processId)
        file_paths += file.fileName
        file_paths += ' '

    return file_paths


def __generate_metalearning_bash_command(process, process_reference):
    train_files = __get_files_path(
        list(filter(lambda file: file.fileType == FileType.TRAIN.value, process.files))
    )
    label_train_files = __get_files_path(
        list(filter(lambda file: file.fileType == FileType.LABEL_TRAIN.value, process.files))
    )
    test_files = __get_files_path(
        list(filter(lambda file: file.fileType == FileType.TEST.value, process.files))
    )
    label_test_files = __get_files_path(
        list(filter(lambda file: file.fileType == FileType.LABEL_TEST.value, process.files))
    )
    sequence_files = __get_files_path(
        list(filter(lambda file: file.fileType == FileType.SEQUENCE.value, process.files))
    )

    output_path_files = __remove_double_bar(output_local_files + process.parametersEntity.output)
    classifier = process.parametersEntity.classifiers
    normalization = process.parametersEntity.normalization
    imbalance = process.parametersEntity.imbalance
    tuning = process.parametersEntity.tuning
    cpu_numbers = process.parametersEntity.cpuNumbers

    bash_command = f'{process_reference} '
    bash_command += f'-train {train_files}'
    bash_command += f'-train_label {label_train_files}'

    if test_files != '':
        bash_command += f'-test {test_files}'
        bash_command += f'-test_label {label_test_files}'

    bash_command += f'-test_nameseq {sequence_files}'
    bash_command += f'-classifier {classifier} '
    bash_command += f'-nf {normalization} '
    bash_command += f'-n_cpu {cpu_numbers} '
    bash_command += f'-imbalance {imbalance} '
    bash_command += f'-tuning {tuning} '
    bash_command += f'-output {output_path_files[:-1]}'

    return str(bash_command)


def __remove_double_bar(string):
    return string.replace('//', '/')


def __decode(process):
    return base64.b64decode(process)
