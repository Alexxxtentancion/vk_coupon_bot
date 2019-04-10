import multiprocessing as mp
import os
import random
import time

import pika
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from NonDaemonPool import MyPool
from qr_gen import remove_img, pdf_generate

token = "6f4e109c2e60f330b15de57da8de7e64a3e809ab8ce43d076e48dd92419d26a9a2a46c1928bac6045c21a"
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 171810806)


def message(**kwargs):
    request = kwargs.get('text')
    print(request)
    image_url = pdf_generate(request)
    print(image_url)
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_messages(image_url)
    if kwargs.get('from_chat'):
        vk.messages.send(
            chat_id=kwargs.get('from_chat'),
            random_id=random.randint(pow(10, 5), pow(10, 6)),
            message="Получите в подарок QR-код Кока-Кола® объемом 0.25 л!",
            attachment='photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])
        )

    elif kwargs.get('from_user'):
        vk.messages.send(
            user_id=kwargs.get('from_user'),
            random_id=random.randint(pow(10, 5), pow(10, 6)),
            message='из лички {}'.format(os.getpid()),
            attachment='photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])
        )

    remove_img(image_url)


if __name__ == '__main__':

    mp.set_start_method('spawn')
    with MyPool(os.cpu_count() * 2) as p:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                begin = time.time()
                if event is not None:
                    kwds = {'text': event.obj.text}
                    if event.from_user:
                        kwds['from_user'] = event.obj.from_id
                    else:
                        kwds['from_chat'] = event.chat_id
                else:
                    kwds = {}
                p.apply_async(func=message, kwds=kwds).get()
                print(time.time() - begin)
    p.close()
    p.join()
