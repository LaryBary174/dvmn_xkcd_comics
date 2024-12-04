import argparse
import asyncio
from pathlib import Path
from utils_for_fetch_imgs import fetch_img_url_comment_xkcd, delete_img
import telegram
from environs import Env


def get_images(folder):
    """Создаем список путей к изображениям в указанной папке"""
    folder_path = Path(folder)
    images = [str(image) for image in folder_path.iterdir() if image.is_file()]
    return images


async def send_images(bot, chat_id, image_path, comment):
    """Отправляем комикс и комментарий в телеграмм"""
    with open(image_path, 'rb') as image:
        await bot.send_document(chat_id=chat_id, document=image, caption=comment)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time', type=int, help='Введите время задержки в секундах', default=3600)
    parser.add_argument('-f', '--folder', help='Путь к папке с изображениями', default='images')

    return parser


async def main():
    url = 'https://xkcd.com/info.0.json'

    env = Env()
    env.read_env()
    bot = telegram.Bot(token=env.str('TELEGRAM_TOKEN'))
    chat_id = env.str('TELEGRAM_CHAT_ID')
    args = create_parser().parse_args()
    time_interval = args.time
    while True:
        images = get_images(args.folder)
        comment = fetch_img_url_comment_xkcd(url, path=args.folder)
        if not images:
            print('Папка пуста')
        else:
            image = images[0]
            try:
                await send_images(bot, chat_id, image, comment)
                delete_img(image)
            except telegram.error.TelegramError:
                print('Не удалось загрузить изображение')

        await asyncio.sleep(time_interval)


if __name__ == '__main__':
    asyncio.run(main())
