import pika


def create_task(ch, _kwargs):
    ch.basic_publish(exchange='',
                     routing_key='img_queue',
                     body=_kwargs,
                     properties=pika.BasicProperties(
                         delivery_mode=2,
                     ))
