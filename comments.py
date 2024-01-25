from googleapiclient.discovery import build
import time
import sys
import logging
from logging import StreamHandler
from typing import Any, List, Union

import telegram

#from exceptions import NoEnvVariable, StatusNot200, TelegramNotAvailable

from settings import (
    RETRY_PERIOD, API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, CHANNEL_ID,
    YOUTUBE_API_VERSION
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_last_2_videos(youtube):
    """Получает ID и названия видео от API YouTUBE."""
    try:
        last_2_videos = youtube.search().list(
            part="snippet",
            channelId=CHANNEL_ID,
            maxResults=2,
            type="video",
            order='date'
            ).execute()
        videos_info = []
        for item in last_2_videos["items"]:
            videos_info.append([item['id']['videoId'], item['snippet']['title']])
        return videos_info
    except:
        logging.error('Нет ответа от API')


def comment_check(youtube, videos_id):
    try:
        blocked = []
        for vidId in videos_id:
            vid_stats = youtube.videos().list(
                part="statistics",
                id=vidId[0]
            ).execute()
            comment_count = vid_stats.get("items")[0].get("statistics").get("commentCount")
            if not comment_count:
                blocked.append(vidId[1])
        return blocked
    except:
        logging.error('Нет ответа от API')


def get_text(blocked: list) -> str:
    """Проверяет статус коментариев и формирует текст сообщения."""
    if not blocked:
        text = 'Ура, с обоими видео всё в порядке!'
    else:
        videos_names = ', '.join(blocked)
        text = 'Комментарии заблокированы к видео: '+ videos_names
    return text


def type_check(text: str, variable: Any, type_: type) -> None:
    """Вызывает исключение, если значение переменной не того типа."""
    if not isinstance(variable, type_):
        raise TypeError(text)


def value_check(item: str, list_: List[str]) -> None:
    """Вызывает исключение, если нет нужного ключа."""
    if item not in list_:
        text = f'Ключа {item} нет в {list_}'
        raise KeyError(text)


def check_tokens() -> None:
    """Проверяет наличие всех переменных окружения."""
    invisible_vars = ''
    env_vars = {
        'API_KEY ': API_KEY,
        'YOUTUBE_API_VERSION ': YOUTUBE_API_VERSION,
        'TELEGRAM_TOKEN ': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID ': TELEGRAM_CHAT_ID,
        'RETRY_PERIOD ': RETRY_PERIOD,
    }
    for key, var in env_vars.items():
        if not var:
            invisible_vars += key
    if invisible_vars != '':
        logging.critical(('Отсутствует обязательная переменная окружения:'
                          f' {invisible_vars}. '
                          'Работа бота принудительно остановлена.'))
        """raise NoEnvVariable(('Отсутствует обязательная'
                            f' переменная окружения: {invisible_vars}'))"""


def send_message(bot: telegram.bot.Bot, message: str) -> Union[bool, None]:
    """Отправляет сообщение в чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(f'Отправлено сообщение: {message}')
        return True
    except telegram.error.NetworkError as error:
        logging.error(f'Не смог отправить сообщение {message} в чат. '
                      f'Телеграм недоступен: {error}')
        #raise TelegramNotAvailable('Телеграм недоступен')
    except telegram.error.TelegramError as error:
        logging.error(f'Не смог отправить сообщение {message} в чат: {error}')
    except Exception as error:
        logging.error(f'Не смог отправить сообщение: {error}')


def main() -> None:
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_message(bot, ('Привет! Я YouTUBE_Bot и буду отслеживать '
                       'статус комментариев к твоим видео :)'))
    bot_working = True
    while bot_working:
        check_tokens()
        youtube = build("youtube", YOUTUBE_API_VERSION, developerKey=API_KEY)
        try:
            videos_id = get_last_2_videos(youtube)
            blocked = comment_check(youtube, videos_id)
            message = get_text(blocked)
            send_message(bot, message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            """if send_message(bot, message):
                last_message[0] = message"""
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='main.log',
        filemode='w',
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        main()
    except KeyboardInterrupt:
        send_message(bot, 'Я выключаюсь. Но скоро снова буду с тобой!')
