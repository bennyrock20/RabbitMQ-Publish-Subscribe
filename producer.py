"""
Class for Producer RabbitMQ client
"""
import os
import json
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_VIRTUAL_HOST = os.getenv("RABBITMQ_VIRTUAL_HOST", "/")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)


class RabbitMQProducer:
    def __init__(self):
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VIRTUAL_HOST, credentials
        )

        self.connection = pika.BlockingConnection(parameters=parameters)

    def publish(
        self,
        routing_key,
        body,
        **kwargs,
    ):
        """
        Publishes a message to the RabbitMQ server
        :param routing_key: The routing key to use
        :param body: The body of the message (python dict)
        """

        channel = self.connection.channel()
        channel.queue_declare(queue=routing_key, durable=True, auto_delete=False)

        # Convert body to json string
        body = json.dumps(body)

        properties = pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2,
            headers={"event_type": routing_key},
        )

        channel.basic_publish(
            exchange="events",
            routing_key=routing_key,
            body=str(body).encode("utf-8"),
            properties=properties,
            **kwargs,
        )
        self.connection.close()

        print(
            " [x] Message Sent to exchange: {} with routing key: {}".format(
                "events", routing_key
            )
        )
