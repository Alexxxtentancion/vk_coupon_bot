import multiprocessing
import os
import pickle
import signal
import pika
from tasks.send_msg import msg_task
from qr_gen import generate_png
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()
script_path = os.path.dirname(os.path.abspath(__file__))

def callback(ch, method, properties, body):
    body = pickle.loads(body)
    body['url'] = generate_png()
    msg_task(channel,body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    channel.queue_declare(queue='img_queue',durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(on_message_callback=callback,
                          queue='img_queue')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass



def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':
    workers = os.cpu_count()
    pool = multiprocessing.Pool(workers,init_worker)
    try:
        for i in range(0, workers):
            pool.apply_async(consume)
        pool.close()
        pool.join()

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()


