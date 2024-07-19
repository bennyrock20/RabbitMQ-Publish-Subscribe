import logging
# from app.celery import app

logger = logging.getLogger(__name__)


# @app.task(queue="events")
def order_created(event_data):
    """
    This function handles the OrderCreated event.
    """
    print(f"OrderCreated event received: {event_data}")

    # Do something with the event data
    # For example, send an email to the customer
    # or update the order status in the database


def handle_event(event_type, event_data):
    """
    This function routes events to the appropriate event handler function based on the event type.
    """

    handlers = {
        "production.OrderCreated": order_created,
    }

    # Look up the handler function for the event type
    handler = handlers.get(event_type)

    if handler:
        # Call the handler function with the event data
        # handler.delay(event_data)
        handler(event_data)
    else:
        logger.info(f"No handler for event type: {event_type}")
