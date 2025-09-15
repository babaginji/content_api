from db import save_content
from news_api import fetch_news

# import requests は YouTube用に必要
import requests
from config import YOUTUBE_API_KEY
import datetime
from typing import List, Dict


# ---------------------------------
# YouTube取得
# ---------------------------------
def fetch_youtube(query="投資", max_results=5, group_type="診断タイプA") -> List[Dict]:
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&maxResults={max_results}&key={YOUTUBE_API_KEY}"
    data = []
    try:
        res = requests.get(url, timeout=10).json()
        for item in res.get("items", []):
            snippet = item["snippet"]
            title = snippet.get("title", "タイトルなし")
            desc = snippet.get("description", "")
            data.append(
                {
                    "type": "YouTube",
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "description": desc,
                    "thumbnail": snippet["thumbnails"]["medium"]["url"],
                    "group_type": group_type,
                    "published_at": snippet.get(
                        "publishedAt", datetime.datetime.now().isoformat()
                    ),
                    "author": snippet.get("channelTitle", "不明"),
                    "ai_comment": "コメント生成はAPI上限で未生成",  # ←安全版
                }
            )
    except Exception as e:
        print(f"[YouTube] データ取得失敗: {e}")
    return data


# ---------------------------------
# News取得
# ---------------------------------
def fetch_news_sample(query="投資", page_size=5, group_type="診断タイプA") -> List[Dict]:
    data = []
    try:
        news_list = fetch_news(query=query, page_size=page_size, group_type=group_type)
        for n in news_list:
            n["ai_comment"] = "コメント生成はAPI上限で未生成"  # ←安全版
            data.append(n)
    except Exception as e:
        print(f"[News] データ取得失敗: {e}")
    return data


# ---------------------------------
# Blog取得
# ---------------------------------
def fetch_blog_sample(group_type="診断タイプA") -> List[Dict]:
    now = datetime.datetime.now().isoformat()
    data = [
        {
            "type": "Blog",
            "title": "初心者向け投資ブログ",
            "url": "https://example.com/blog1",
            "description": "分かりやすく投資の基本を解説",
            "thumbnail": "",
            "group_type": group_type,
            "published_at": now,
            "author": "ブログ作者A",
            "ai_comment": "コメント生成はAPI上限で未生成",
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
            "ai_comment": "コメント生成はAPI上限で未生成",
        },
    ]
    return data


# ---------------------------------
# メイン
# ---------------------------------
def main(group_type="診断タイプA"):
    all_data = []
    all_data.extend(fetch_youtube(group_type=group_type))
    all_data.extend(fetch_news_sample(group_type=group_type))
    all_data.extend(fetch_blog_sample(group_type=group_type))

    if all_data:
        save_content(all_data)
        print(f"{len(all_data)} 件のコンテンツをDBに追加しました！")
    else:
        print("追加するコンテンツがありませんでした。")


if __name__ == "__main__":
    main()
