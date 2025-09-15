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
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            title TEXT,
            url TEXT,
            description TEXT,
            thumbnail TEXT,
            group_type TEXT,
            published_at TEXT,
            author TEXT,
            likes INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()
    print("DBを初期化しました！")


# ---------------------------
# コンテンツ保存
# ---------------------------
def save_content(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in data:
        c.execute(
            """
            INSERT INTO content (type, title, url, description, thumbnail, group_type, published_at, author)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )
    conn.commit()
    conn.close()
    print("サンプルデータを登録しました！")


# ---------------------------
# グループ別コンテンツ取得
# ---------------------------
def get_content_by_group(group_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, type, title, url, description, thumbnail, group_type, published_at, author, likes
        FROM content
        WHERE group_type=?
        """,
        (group_type,),
    )
    rows = c.fetchall()
    conn.close()
    return rows


# ---------------------------
# ID指定でコンテンツ取得
# ---------------------------
def get_content_by_id(content_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, type, title, url, description, thumbnail, group_type, published_at, author, likes
        FROM content
        WHERE id=?
        """,
        (content_id,),
    )
    row = c.fetchone()
    conn.close()
    return row


# ---------------------------
# いいね関連
# ---------------------------
def get_likes(content_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT likes FROM content WHERE id=?", (content_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0


def add_like(content_id):
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
