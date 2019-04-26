
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()


def create_task(_kwargs):
    channel.basic_publish(exchange='',
                          routing_key='img_queue',
                          body=_kwargs,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))
