import os
import json
import logging
from social_net.vk_request import VkRequest
from social_net.yandex import Yandex


def get_token(file_name):
    with open(os.path.join(os.getcwd(), file_name), 'r') as token_file:
        token = token_file.readline().strip()
    return token


# Можно проверять валидные значения
def get_vk_id():
    while True:
        try:
            return int(input('Введите id пользователя: '))
        except ValueError:
            logging.error('Ошибка. Необходимо ввести цифровое значение')


def photo_count(default_count: int = 5):
    while True:
        try:
            return int(input(f'Введите количество загружаемых фото [{default_count}]: ') or default_count)
        except ValueError:
            logging.error('Ошибка. Необходимо ввести цифровое значение')


if __name__ == "__main__":
    tokenVK = 'VK_TOKEN.txt'
    tokenYandex = 'Ya_TOKEN.txt'

    yandex_token = get_token(tokenYandex)
    vk_token = get_token(tokenVK)
    vk_user_id = get_vk_id()
    max_count = photo_count()
    test_VK = VkRequest(vk_token, vk_user_id)

    with open('VK_photo.json', 'w') as outfile:
        json.dump(test_VK.json, outfile)

    my_yandex = Yandex('VK photo copies', yandex_token, max_count)
    my_yandex.create_copy(test_VK.export_dict)
