import openai
from config import OPENAI_API_KEY
from typing import Optional

openai.api_key = OPENAI_API_KEY


def generate_comment(title: str, description: str, user_type: str) -> str:
    """
    指定記事を user_type 向けに簡単に解説したコメントを生成
    """
    prompt = f"次の記事を {user_type} 向けに簡単に解説して: {title}\n{description}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=60, temperature=0.7
        )
        comment = response.choices[0].text.strip()
        return comment if comment else "コメントが生成できませんでした。"
    except Exception as e:
        print(f"[OpenAI] コメント生成失敗: {e}")
        return "コメント生成中にエラーが発生しました。"
