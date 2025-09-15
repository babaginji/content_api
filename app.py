from flask import Flask, render_template, request, redirect, url_for
from db import get_content_by_group, init_db, add_like, get_content_by_id
from apscheduler.schedulers.background import BackgroundScheduler
from fetch_and_save_content import main as fetch_content
from ai_comment import generate_comment  # AIコメント用関数

import atexit

app = Flask(__name__)

# DB初期化（最初だけ）
init_db()

# ---------------------------
# スケジューラー起動
# ---------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_content, "interval", minutes=10)  # 10分ごとに取得
scheduler.start()

# ---------------------------
# Jinja から AI コメント関数を呼べるように
# ---------------------------
app.jinja_env.globals["generate_comment"] = generate_comment

# ---------------------------
# ルート定義
# ---------------------------
@app.route("/")
def home():
    group_type = request.args.get("group_type", "診断タイプA")
    contents = get_content_by_group(group_type)
    return render_template("content_feed.html", contents=contents)


@app.route("/content/<int:content_id>")
def content_detail(content_id):
    content = get_content_by_id(content_id)
    if not content:
        return "コンテンツが見つかりません", 404
    return render_template("content_detail.html", content=content)


@app.route("/like/<int:content_id>", methods=["POST"])
def like_content(content_id):
    add_like(content_id)
    return redirect(request.referrer or url_for("home"))


# ---------------------------
# アプリ終了時にスケジューラー停止
# ---------------------------
atexit.register(lambda: scheduler.shutdown())

# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
