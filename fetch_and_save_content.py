from db import save_content
from news_api import fetch_news
import requests
from config import YOUTUBE_API_KEY
import datetime

# ---------------------------
# YouTube検索サンプル
# ---------------------------
def fetch_youtube(query="投資", max_results=3):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&q={query}&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    )
    res = requests.get(url).json()
    data = []
    for item in res.get("items", []):
        snippet = item["snippet"]
        data.append(
            {
                "type": "YouTube",
                "title": snippet["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "description": snippet.get("description", ""),
                "thumbnail": snippet["thumbnails"]["medium"]["url"],
                "group_type": "typeA",  # 仮の診断タイプ
                "published_at": snippet.get(
                    "publishedAt", datetime.datetime.now().isoformat()
                ),
                "author": snippet.get("channelTitle", "不明"),
            }
        )
    return data


# ---------------------------
# News取得サンプル
# ---------------------------
def fetch_news_sample(query="投資", page_size=3):
    return fetch_news(query=query, page_size=page_size)


# ---------------------------
# Blog取得サンプル（簡易版）
# ---------------------------
def fetch_blog_sample():
    # 本番ではRSSや独自APIから取得
    data = [
        {
            "type": "Blog",
            "title": "初心者向け投資ブログ",
            "url": "https://example.com/blog1",
            "description": "分かりやすく投資の基本を解説",
            "thumbnail": "",
            "group_type": "typeA",
            "published_at": datetime.datetime.now().isoformat(),
            "author": "ブログ作者A",
        },
        {
            "type": "Blog",
            "title": "中級者向け投資戦略",
            "url": "https://example.com/blog2",
            "description": "リスク管理と分散投資を丁寧に説明",
            "thumbnail": "",
            "group_type": "typeB",
            "published_at": datetime.datetime.now().isoformat(),
            "author": "ブログ作者B",
        },
    ]
    return data


# ---------------------------
# DBに保存
# ---------------------------
def main():
    all_data = []
    all_data.extend(fetch_youtube())
    all_data.extend(fetch_news_sample())
    all_data.extend(fetch_blog_sample())

    save_content(all_data)
    print("コンテンツをDBに追加しました！")


if __name__ == "__main__":
    main()
