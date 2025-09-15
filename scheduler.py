from apscheduler.schedulers.background import BackgroundScheduler
from fetch_and_save_content import main as fetch_content
import time


def start_scheduler():
    scheduler = BackgroundScheduler()
    # 例：10分ごとにコンテンツ取得
    scheduler.add_job(fetch_content, "interval", minutes=10)
    scheduler.start()
    print("コンテンツ自動取得スケジューラーを起動しました")

    try:
        while True:
            time.sleep(60)  # メインスレッドを保持
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("スケジューラーを停止しました")


if __name__ == "__main__":
    start_scheduler()
