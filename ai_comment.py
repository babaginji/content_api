import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def generate_comment(title: str, description: str, user_type: str) -> str:
    """
    指定記事を user_type 向けに簡単に解説したコメントを生成
    API利用不可時は安全にデフォルトコメントを返す
    """
    prompt = f"次の記事を {user_type} 向けに簡単に解説して: {title}\n{description}"

    try:
        # 新しい Chat Completions API を使用
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7,
        )
        comment = response.choices[0].message.content.strip()
        return comment if comment else "コメントが生成できませんでした。"
    except Exception as e:
        # APIエラー時はデフォルトコメント
        print(f"[OpenAI] コメント生成失敗: {e}")
        return "この記事についてのコメントは準備中です。"
