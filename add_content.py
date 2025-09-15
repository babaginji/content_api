from db import save_content
from datetime import datetime

# ---------------------------
# サンプルデータ作成
# ---------------------------
sample_data = []

# YouTubeサンプル 10件
for i in range(10):
    sample_data.append(
        {
            "type": "YouTube",
            "title": f"サンプルYouTube動画 {i+1}",
            "url": f"https://www.youtube.com/watch?v=sample{i+1}",
            "description": f"これはYouTubeのサンプル動画説明 {i+1}",
            "thumbnail": "",
            "group_type": "診断タイプA",
            "published_at": datetime.now().isoformat(),
            "author": "YouTube Author",
        }
    )

# Newsサンプル 10件
for i in range(10):
    sample_data.append(
        {
            "type": "News",
            "title": f"サンプルニュース {i+1}",
            "url": f"https://news.example.com/article{i+1}",
            "description": f"これはニュースのサンプル説明 {i+1}",
            "thumbnail": "",
            "group_type": "診断タイプA",
            "published_at": datetime.now().isoformat(),
            "author": "News Author",
        }
    )

# Blogサンプル 10件
for i in range(10):
    sample_data.append(
        {
            "type": "Blog",
            "title": f"サンプルブログ {i+1}",
            "url": f"https://blog.example.com/post{i+1}",
            "description": f"これはブログのサンプル説明 {i+1}",
            "thumbnail": "",
            "group_type": "診断タイプA",
            "published_at": datetime.now().isoformat(),
            "author": "Blog Author",
        }
    )

# AIコメントサンプル 10件
for i in range(10):
    sample_data.append(
        {
            "type": "AIコメント",
            "title": f"サンプルAIコメント {i+1}",
            "url": "",
            "description": f"これはAIコメントのサンプル説明 {i+1}",
            "thumbnail": "",
            "group_type": "診断タイプA",
            "published_at": datetime.now().isoformat(),
            "author": "AI",
        }
    )

# ---------------------------
# DBに保存
# ---------------------------
save_content(sample_data)
print("サンプルコンテンツをまとめて追加しました！")
