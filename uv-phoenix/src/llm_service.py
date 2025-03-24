import os
from openai import OpenAI
from tools import TOOL_DESCRIPTIONS


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """あなたは有能なアシスタントです。ユーザーに対して親身に寄り添ってください。
もしユーザーが、DBへのアクセスを要求した場合、ユーザーの認証を行ってからDBへのアクセスを行ってください。
ユーザーの認証に失敗した場合、ユーザーに対してその旨を伝えてください。
ユーザーの認証に成功した場合、DBへのアクセスを行うまえに、認証に成功したことをユーザーに伝えてください。
その上で DB 上でユーザーが要求した操作を行ってください。
"""


def get_response(messages):
    system_prompt = {"role": "system", "content": SYSTEM_PROMPT}
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_prompt] + messages,
        tools=TOOL_DESCRIPTIONS,
        tool_choice="auto",
    )
    return response