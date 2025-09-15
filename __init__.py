from flask import Blueprint

content_api_bp = Blueprint(
    "content_api", __name__, template_folder="templates", static_folder="static"
)

from . import views  # 後で作成するルート定義
