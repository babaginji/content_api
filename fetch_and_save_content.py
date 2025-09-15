from db import save_content
from news_api import fetch_news
import requests
from config import YOUTUBE_API_KEY
import datetime
from typing import List, Dict

# ---------------------------
# YouTube検索
# ---------------------------
def fetch_youtube(
    query: str = "投資", max_results: int = 3, group_type: str = "診断タイプA"
) -> List[Dict]:
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&q={query}&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    )
    data = []
    try:
        res = requests.get(url, timeout=10).json()
        for item in res.get("items", []):
            snippet = item["snippet"]
            data.append(
                {
                    "type": "YouTube",
                    "title": snippet.get("title", "タイトルなし"),
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "description": snippet.get("description", ""),
                    "thumbnail": snippet["thumbnails"]["medium"]["url"],
                    "group_type": group_type,
                    "published_at": snippet.get(
                        "publishedAt", datetime.datetime.now().isoformat()
                    ),
                    "author": snippet.get("channelTitle", "不明"),
                }
            )
    except Exception as e:
        print(f"[YouTube] データ取得失敗: {e}")
    return data


# ---------------------------
# News取得
# ---------------------------
def fetch_news_sample(
    query: str = "投資", page_size: int = 3, group_type: str = "診断タイプA"
) -> List[Dict]:
    try:
        return fetch_news(query=query, page_size=page_size, group_type=group_type)
    except Exception as e:
        print(f"[News] データ取得失敗: {e}")
        return []


# ---------------------------
# Blog取得（簡易版）
# ---------------------------
def fetch_blog_sample() -> List[Dict]:
    now = datetime.datetime.now().isoformat()
    data = [
        {
            "type": "Blog",
            "title": "初心者向け投資ブログ",
            "url": "https://example.com/blog1",
            "description": "分かりやすく投資の基本を解説",
            "thumbnail": "",
            "group_type": "診断タイプA",
            "published_at": now,
            "author": "ブログ作者A",
        },
        {
            "type": "Blog",
            "title": "中級者向け投資戦略",
            "url": "https://example.com/blog2",
            "description": "リスク管理と分散投資を丁寧に説明",
            "thumbnail": "",
            "group_type": "診断タイプB",
            "published_at": now,
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

    if all_data:
        save_content(all_data)
        print("コンテンツをDBに追加しました！")
    else:
        print("追加するコンテンツがありませんでした。")


# ---------------------------
if __name__ == "__main__":
    main()
