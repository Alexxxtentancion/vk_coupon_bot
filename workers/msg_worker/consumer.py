import pika
import time
from vk_bot import send_message
import pickle
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()

def callback(ch, method, properties, body):
    send_message(pickle.loads(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)




def consume():
    channel.queue_declare(queue='vk_queue',durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(on_message_callback=callback,
                          queue='vk_queue')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    consume()
