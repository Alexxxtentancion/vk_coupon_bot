import os
import pickle
import random
import  multiprocessing as ms
import pika
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from qr_gen import remove_img, generate_png

token = "6f4e109c2e60f330b15de57da8de7e64a3e809ab8ce43d076e48dd92419d26a9a2a46c1928bac6045c21a"
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 171810806)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue', durable=True)


def create_message():
    image_url = generate_png()
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_messages(image_url)
    photo = 'photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])
    return image_url, photo


def send_message(body):
    image_url, attachment = create_message()
    if body.get('from_chat'):
        vk.messages.send(
            chat_id=body.get('from_chat'),
            random_id=random.randint(pow(10, 5), pow(10, 6)),
            message="Держите купон",
            attachment=attachment
        )

    elif body.get('from_user'):
        vk.messages.send(
            user_id=body.get('from_user'),
            random_id=random.randint(pow(10, 5), pow(10, 6)),
            message='из лички {}'.format(ms.current_process().name),
            attachment=attachment
        )

    remove_img(image_url)


def create_task(_kwargs):
    channel.basic_publish(exchange='',
                          routing_key='queue',
                          body=_kwargs,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))


if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event is not None:
                _kwargs = {'text': event.obj.text}
                if event.from_user:
                    _kwargs['from_user'] = event.obj.from_id
                else:
                    _kwargs['from_chat'] = event.chat_id
            else:
                _kwargs = {}
            create_task(pickle.dumps(_kwargs))
