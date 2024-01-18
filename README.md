# YouTube Creator Bot

### Описание проекта youtube-bot
Youtube-bot - это бот в Телеграм для проверки того, были ли отключены комментарии к видео (т.к. Youtube периодически их без уведомлений отключает). Каждые 10 минут бот делает запрос к API YouTube и, если комментарии к одному из двух последних видео отключены, то сообщает об этом в телеграм.
Проект для практики работы с YouTube API.

### Как запустить проект:

Создать телеграм-бот:

* добавить в ТГ @BotFather (с галочкой)
* команда /newbot
* указать имя и техническое имя бота (уникальное и должно заканчиваться на bot)
* @BotFather пришлет токен TELEGRAM_TOKEN
* настроить инфу о боте
* добавить своего бота в ТГ (найти по техническому имени)

Получить API-ключ для YouTube:

* в https://console.cloud.google.com/ создать новый проект
* активировать (кнопка «Enable») на проекте «YouTube Data API v3» (найти через поисковую строку)
* в меню слева выбрать «Credentials» -> «Create credentials» -> «API key». Скопировать ключ

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MiladyEmily/youtube_creator_bot
```

```
cd youtube_creator_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать файл .env и заполнить в нём следующие :

* API_KEY    :    получен в через гугл-консоль
* CHANNEL_ID     :     получить из URL главной страницы канала
* TELEGRAM_TOKEN     :    получен при регистрации бота
* TELEGRAM_CHAT_ID   :    добавить в ТГ бота @userinfobot, в ответ пришлет ID

Запустить проект:

```
python comments.py
```
