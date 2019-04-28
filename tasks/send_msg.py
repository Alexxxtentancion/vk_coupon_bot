import pickle

import pika


def msg_task(ch, body):
    ch.basic_publish(exchange='',
                     routing_key='vk_queue',
                     body=pickle.dumps(body),
                     properties=pika.BasicProperties(
                         delivery_mode=2,
                     ))
