import os
import pika
import time

RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "user")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "QqQNcTYGaeNUpjDS")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE", "myqueue")

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

for i in range(10):
    message = f"Task {i}"
    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(f"[x] Sent {message}")
    time.sleep(0.5)

connection.close()
