from datetime import datetime
from os import environ
import logging
import traceback

import pika

from ThreadPoolService import ThreadPoolService
from init_process_service import start


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

address = environ.get("APP_AMQP_ADDRESS")
amount_workers = environ.get("APP_WORKERS")
thread_poll = ThreadPoolService(amount_workers)


def start_consume():
    parameters = pika.connection.URLParameters(address)
    parameters.socket_timeout = 5

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.basic_consume('baml.processes.init',
                          callback,
                          auto_ack=True)

    channel.start_consuming()


def callback(ch, method, properties, body):
    try:
        logger.info("received " + body.__str__() + " at " + datetime.now().__str__())
        thread = thread_poll.get_worker()
        thread.submit(start, body)
        logger.info("released thread=", thread.__str__())
    except Exception as e:
        logger.error("Exception %s: %s" % (type(e), e))
        logger.debug(traceback.format_exc())


if __name__ == "__processes_consumer__":
    start_consume()
