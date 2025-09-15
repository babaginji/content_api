from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY


def fetch_youtube_videos(query="finance", max_results=5):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    req = youtube.search().list(
        q=query, part="snippet", type="video", maxResults=max_results
    )
    res = req.execute()
    data = []
    for item in res.get("items", []):
        data.append(
            {
                "type": "youtube",
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                "group_type": "typeA",  # 仮にtypeAに割り当て
            }
        )
    return data
