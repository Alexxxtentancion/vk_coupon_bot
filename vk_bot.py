import multiprocessing as ms
import pickle
import random

import pika
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from qr_gen import remove_img
from tasks.create_msg import create_task
from mytoken import tokengit
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 171810806)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='img_queue', durable=True)


def send_message(body):
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_messages(body.get('url'))
    photo = 'photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])

    if body.get('from_chat'):
        vk.messages.send(
            chat_id=body.get('from_chat'),
            random_id=random.randint(pow(10, 5), pow(10, 6)),
            message="Держите купон",
            attachment=photo
        )

    elif body.get('from_user'):
        vk.messages.send(
            user_id=body.get('from_user'),
            random_id=random.randint(pow(10, 5), pow(10, 6)),
            message='из лички {}'.format(ms.current_process().name),
            attachment=photo
        )
    remove_img(body.get('url'))


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
            create_task(channel, pickle.dumps(_kwargs))
