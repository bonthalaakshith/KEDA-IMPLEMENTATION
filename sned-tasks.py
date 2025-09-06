import pika

RABBITMQ_HOST = "localhost"  # or the NodePort / port-forward host
RABBITMQ_USER = "user"
RABBITMQ_PASSWORD = "QqQNcTYGaeNUpjDS"
QUEUE_NAME = "myqueue"

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

for i in range(300):
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=f'Task {i}')
    print(f"[x] Sent Task {i}")

connection.close()
