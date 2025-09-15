import openai
from config import OPENAI_API_KEY
from typing import Optional

# OpenAI APIキー設定
openai.api_key = OPENAI_API_KEY


def generate_comment(title: str, description: str, user_type: str) -> str:
    """
    指定記事を user_type 向けに簡単に解説したコメントを生成
    feed 画面や詳細画面で表示可能
    """
    prompt = f"""
次の記事を {user_type} 向けに簡単に解説してください。文章は短く、親しみやすくしてください。
タイトル: {title}
内容: {description}
"""
    try:
        # 完全版では max_tokens や temperature を調整して柔軟に
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=80,  # 少し余裕をもたせて読みやすく
            temperature=0.7,  # 創造性を維持
            top_p=1.0,
            n=1,
            stop=None,
        )
        comment = response.choices[0].text.strip()
        return comment if comment else "コメントが生成できませんでした。"
    except Exception as e:
        print(f"[OpenAI] コメント生成失敗: {e}")
        return "コメント生成中にエラーが発生しました。"
