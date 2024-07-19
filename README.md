# RabbitMQ Scripts

This repository contains two Python scripts for demonstrating the basic usage of RabbitMQ: a producer and a consumer.

## Requirements

- docker
- docker-compose

## Usage

1. Start the RabbitMQ server and consumer

```bash
docker-compose up
```
2. Run the producer script using the following command:

```bash
 docker-compose run consumer python send_message.py
```
