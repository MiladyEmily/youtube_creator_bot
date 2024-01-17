from googleapiclient.discovery import build

from settings import (
    RETRY_PERIOD, API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, CHANNEL_ID,
    YOUTUBE_API_VERSION
)


youtube = build("youtube", YOUTUBE_API_VERSION, developerKey=API_KEY)
last_2_videos = youtube.search().list(
    part="snippet",
    channelId=CHANNEL_ID,
    maxResults=2,
    type="video",
    order='date'
    ).execute()
videos_id = []
for item in last_2_videos["items"]:
    videos_id.append(item['id']['videoId'])
for vidId in videos_id:
    vid_stats = youtube.videos().list(
        part="statistics",
        id=vidId
    ).execute()
    comment_count = vid_stats.get("items")[0].get("statistics").get("commentCount")
    if not comment_count:
        print('Комментарии заблокированы!')
