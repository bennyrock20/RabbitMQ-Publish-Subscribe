import pika
import os
import time
from pika.exceptions import AMQPConnectionError

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_VIRTUAL_HOST = os.getenv("RABBITMQ_VIRTUAL_HOST", "/")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)


class RabbitMQConsumer:
    def __init__(self):
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(
            RABBITMQ_HOST,
            RABBITMQ_PORT,
            RABBITMQ_VIRTUAL_HOST,
            credentials,
            heartbeat=0,
        )

    def start_consuming(self, queue, callback):
        """
        Starts consuming messages from the RabbitMQ server and calls the callback function
        """
        while True:
            try:
                connection = pika.BlockingConnection(parameters=self.parameters)
                channel = connection.channel()

                exchange_name = "events"
                channel.exchange_declare(exchange=exchange_name, exchange_type="topic")
                channel.queue_declare(queue=queue, durable=True, auto_delete=False)
                channel.queue_bind(exchange=exchange_name, queue=queue, routing_key="#")
                channel.basic_consume(queue=queue, on_message_callback=callback)
                channel.start_consuming()
            except AMQPConnectionError as e:
                print("Lost connection to RabbitMQ, reconnecting...", e)
                time.sleep(3)
