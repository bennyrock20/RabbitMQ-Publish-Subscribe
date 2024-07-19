import json
import logging

from django.core.management.base import BaseCommand
from event_handler.event import handle_event

logger = logging.getLogger(__name__)


def callback(channel, method, properties, body):
    try:
        # Parse the event data from JSON
        event_data = json.loads(body)

        # Get the event type from the headers
        headers = properties.headers
        event_type = (
            headers["event_type"] if headers and "event_type" in headers else None
        )

        logger.info(f"Received event: {event_type}")

        # Handle the event
        handle_event.delay(event_type=event_type, event_data=event_data)

        # Acknowledge the message to RabbitMQ
        channel.basic_ack(method.delivery_tag)
    except Exception as e:
        # Acknowledge the message to RabbitMQ to avoid requeueing
        channel.basic_nack(method.delivery_tag, requeue=False)
        print("Error handling event:", e)
        logger.error(e)


class Command(BaseCommand):
    help = "Starts RabbitMQ Consumer"

    def handle(self, *args, **options):
        from consumer import RabbitMQConsumer

        print("Starting Event Handler Consumer...")
        consumer = RabbitMQConsumer()
        consumer.start_consuming(queue="event_handler", callback=callback)
