import base64

from ..classes.Producer import Producer
from ..classes.ErrorHandler import ErrorHandler
from ..services.logger_service import get_logger

queue = 'baml.processes.errors'
logger = get_logger('error_producer')


def send_error(ex: Exception, process_id):
    error_handler = ErrorHandler(
        ex.__class__.__name__,
        str(ex),
        process_id
    )

    logger.info(f'send error message={error_handler.__dict__}')

    message = error_handler.to_json()
    logger.info(f'error message={message}')

    encoded_message = base64.b64encode(message.encode())
    logger.info(f'send error message encoded={encoded_message}')

    producer = Producer()
    producer.send(
        queue=queue,
        message=encoded_message
    )
