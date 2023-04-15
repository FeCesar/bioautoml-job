from os import environ

import pika


class Producer:

    def __init__(self):
        self.address = environ.get("APP_AMQP_ADDRESS")
        self.parameters = pika.connection.URLParameters(self.address)
        self.parameters.socket_timeout = 5

        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def send(self, queue, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message
        )
