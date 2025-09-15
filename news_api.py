import requests
from config import NEWS_API_KEY
from typing import List, Dict


def fetch_news(
    query: str = "finance", page_size: int = 5, group_type: str = "診断タイプA"
) -> List[Dict]:
    """
    NewsAPIからニュース記事を取得してリスト形式で返す
    """
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
    except Exception as e:
        print(f"[NewsAPI] ニュース取得失敗: {e}")
        articles = []

    data = []
    for a in articles:
        data.append(
            {
                "type": "news",
                "title": a.get("title", "タイトルなし"),
                "url": a.get("url", "#"),
                "description": a.get("description", ""),
                "thumbnail": a.get("urlToImage", ""),
                "group_type": group_type,  # 引数で動的に設定可能
            }
        )
    return data
