import base64

from ..classes.Producer import Producer
from ..services.logger_service import get_logger
from ..classes.UpdateStatusVO import UpdateStatusVO

queue = 'baml.processes.status'
logger = get_logger('error_producer')


def update_status(status, process_id):
    update_status_vo = UpdateStatusVO(
        status,
        process_id
    )

    message = update_status_vo.to_json()
    logger.info(f'update process status message={message}')

    encoded_message = base64.b64encode(message.encode())
    logger.info(f'send process status message encoded={encoded_message}')

    producer = Producer()
    producer.send(
        queue=queue,
        message=encoded_message
    )
