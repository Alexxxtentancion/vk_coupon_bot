import pickle

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()


def msg_task(body):
    channel.basic_publish(exchange='',
                          routing_key='vk_queue',
                          body=pickle.dumps(body),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))
