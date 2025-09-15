import requests
from config import NEWS_API_KEY


def fetch_news(query="finance", page_size=5):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    data = []
    for a in articles:
        data.append(
            {
                "type": "news",
                "title": a.get("title", "タイトルなし"),
                "url": a.get("url", "#"),
                "description": a.get("description", ""),
                "thumbnail": a.get("urlToImage", ""),
                "group_type": "typeA",  # 仮に typeA に割り当て
            }
        )
    return data
