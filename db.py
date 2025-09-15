import sqlite3
from config import DB_PATH
from datetime import datetime

# ---------------------------
# DB初期化
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        DROP TABLE IF EXISTS content;
        """
    )
    c.execute(
        """
        CREATE TABLE content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            title TEXT,
            url TEXT,
            description TEXT,
            thumbnail TEXT,
            group_type TEXT,
            published_at TEXT,
            author TEXT,
            likes INTEGER DEFAULT 0,
            ai_comment TEXT
        )
        """
    )
    conn.commit()
    conn.close()
    print("DBを初期化しました（ai_commentカラム付き）！")


# ---------------------------
# コンテンツ保存（重複チェック付き）
# data は list of dict
# ---------------------------
def save_content(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in data:
        # URL or タイトルが重複していないか確認
        c.execute(
            "SELECT id FROM content WHERE url=? OR title=?",
            (item["url"], item["title"]),
        )
        if c.fetchone():
            continue  # 既にある場合はスキップ

        c.execute(
            """
            INSERT INTO content (type, title, url, description, thumbnail, group_type, published_at, author, ai_comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["type"],
                item["title"],
                item["url"],
                item.get("description", ""),
                item.get("thumbnail", ""),
                item["group_type"],
                item.get("published_at", datetime.now().isoformat()),
                item.get("author", ""),
                item.get("ai_comment", ""),
            ),
        )
    conn.commit()
    conn.close()
    print(f"{len(data)} 件のコンテンツを保存しました（重複は除外）")


# ---------------------------
# グループ別コンテンツ取得
# ---------------------------
def get_content_by_group(group_type: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, type, title, url, description, thumbnail, group_type, published_at, author, likes, ai_comment
        FROM content
        WHERE group_type=?
        ORDER BY published_at DESC
        """,
        (group_type,),
    )
    rows = c.fetchall()
    conn.close()
    return rows  # list of tuple


# ---------------------------
# ID指定でコンテンツ取得
# ---------------------------
def get_content_by_id(content_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, type, title, url, description, thumbnail, group_type, published_at, author, likes, ai_comment
        FROM content
        WHERE id=?
        """,
        (content_id,),
    )
    row = c.fetchone()
    conn.close()
    return row  # tuple or None


# ---------------------------
# いいね関連
# ---------------------------
def get_likes(content_id: int) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT likes FROM content WHERE id=?", (content_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0


def add_like(content_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE content SET likes = likes + 1 WHERE id=?", (content_id,))
    conn.commit()
    conn.close()


# ---------------------------
# 実行用
# ---------------------------
if __name__ == "__main__":
    init_db()
