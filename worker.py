import multiprocessing
import os
import pickle
import time

import pika

from vk_bot import send_message


def callback(ch, method, properties, body):
    begin = time.time()
    send_message(pickle.loads(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(time.time() - begin)


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='queue', durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(on_message_callback=callback,
                          queue='queue')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    workers = os.cpu_count() * 2 - 1
    pool = multiprocessing.Pool(processes=workers)
    for i in range(0, workers):
        pool.apply_async(consume)
    try:
        while True:
            continue
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
