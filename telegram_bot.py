import argparse
import os
from multiprocessing.managers import Value
from pathlib import Path
from utils_for_fetch_imgs import fetch_img_url_comment_xkcd, delete_img
import telegram
from environs import Env


def send_images(bot, chat_id, image_path, comment):
    """Отправляем комикс и комментарий в телеграмм"""
    with open(image_path, 'rb') as image:
        bot.send_document(chat_id=chat_id, document=image, caption=comment)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', help='Путь к папке с изображениями', default='images')

    return parser


def main():
    url = 'https://xkcd.com/info.0.json'
    env = Env()
    env.read_env()
    bot = telegram.Bot(token=env.str('TELEGRAM_TOKEN'))
    chat_id = env.str('TELEGRAM_CHAT_ID')
    args = create_parser().parse_args()
    image_folder = os.path.join(args.folder)
    os.makedirs(image_folder, exist_ok=True)
    folder_path = Path(args.folder)
    images = folder_path.iterdir()
    comment = fetch_img_url_comment_xkcd(url, image_folder)
    for image in images:
        if image.is_file():
            try:
                send_images(bot, chat_id, image, comment)
            except telegram.error.TelegramError:
                print('Не удалось загрузить изображение')
            finally:
                delete_img(image)
        else:
            print('Папка пуста')


if __name__ == '__main__':
    main()
