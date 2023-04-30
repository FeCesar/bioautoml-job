import base64

from ..classes.Producer import Producer
from ..classes.ProcessResult import ProcessResult
from ..services.logger_service import get_logger

queue = 'baml.processes.results'
logger = get_logger('generate_result_producer')


def send_result(process_id):
    process_result = ProcessResult(
        process_id
    )

    message = process_result.to_json()
    logger.info(f'process result message={message}')

    encoded_message = base64.b64encode(message.encode())
    logger.info(f'send process result message encoded={encoded_message}')

    producer = Producer()
    producer.send(
        queue=queue,
        message=encoded_message
    )
