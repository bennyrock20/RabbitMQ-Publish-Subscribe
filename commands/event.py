import logging
from app.celery import app
from tasks.product_events import order_created

logger = logging.getLogger(__name__)


@app.task(bind=True, queue="events")
def handle_event(self, event_type, event_data):
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
        handler(event_data)
    else:
        logger.info(f"No handler for event type: {event_type}")
