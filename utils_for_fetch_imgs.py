import os.path
import random
from urllib.parse import urlparse

import requests


def download_image(filename: str, url: str, params: dict = None, image_folder:str = None):
    """Загружаем картинку с url, принимает параметры если необходимо """
    path_to_jpeg = os.path.join(image_folder, f'{filename}{expand_file(url)}')
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    with open(path_to_jpeg, 'wb') as f:
        f.write(response.content)


def expand_file(url: str):
    """ Определяем формат"""
    parsed_url = urlparse(url)

    return os.path.splitext(parsed_url.path)[1]


def get_random_comics_num(url: str):
    """ Получение номера комикса случайным образом"""
    response = requests.get(url)
    response.raise_for_status()
    xkcd_nums = response.json()['num']
    random_xkcd_num = random.randint(1, xkcd_nums)
    return random_xkcd_num


def fetch_img_url_comment_xkcd(url: str, image_folder: str = 'images'):
    """ Загружаем комикс со случайным номером и получаем комментарий автора к этому комиксу"""
    nums = get_random_comics_num(url)
    url_nums = f'https://xkcd.com/{nums}/info.0.json'
    response = requests.get(url_nums)
    response.raise_for_status()
    xkcd_response = response.json()
    xkcd_comics_url = xkcd_response['img']
    download_image('xkcd_comic', xkcd_comics_url, image_folder=image_folder)
    comment = xkcd_response['alt']
    return comment


def delete_img(img_path: str):
    """Удаление файла"""
    if os.path.exists(img_path):
        os.remove(img_path)


