import os
import pika
import time

RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE", "myqueue")

parameters = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
)

while True:
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        def callback(ch, method, properties, body):
            print(f"[x] Received {body.decode()}")
            time.sleep(1)  # simulate processing time
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        print(f"Connection error: {e}, retrying in 5s...")
        time.sleep(5)
