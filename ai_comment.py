import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_comment(title, description, user_type):
    prompt = f"次の記事を {user_type} 向けに簡単に解説して: {title}\n{description}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60
    )
    return response.choices[0].text.strip()
