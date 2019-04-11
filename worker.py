import multiprocessing
import os
import pickle
import time

import pika

from vk_bot import send_message,create_message

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()


def callback(ch, method, properties, body):
    body = pickle.loads(body)
    body['attachment'] = create_message()
    msg_task(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume():
    channel.queue_declare(queue='img_queue', durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(on_message_callback=callback,
                          queue='img_queue')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass


def msg_task(body):
    channel.basic_publish(exchange='',
                          routing_key='vk_queue',
                          body=pickle.dumps(body),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))


if __name__ == '__main__':
    workers = os.cpu_count()
    pool = multiprocessing.Pool(processes=workers)
    for i in range(0, workers):
        pool.apply_async(consume)
    try:
        while True:
            continue
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
