import os

from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
RETRY_PERIOD = 600
YOUTUBE_API_VERSION = "v3"
#ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
#HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
