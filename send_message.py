import json

if __name__ == "__main__":
    from utils.producer import RabbitMQProducer

    producer = RabbitMQProducer()

    message = {"order_number": "123"}

    producer.publish(
        routing_key="production.OrderCreated", body=json.dumps(message)
    )
