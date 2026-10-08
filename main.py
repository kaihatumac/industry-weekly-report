import os
import requests
from google import genai


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]


def generate_report():
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = """
あなたは製餡・和菓子・洋菓子・パン業界に詳しい
食品業界の経営アナリストです。

松原製餡所の営業・経営判断に役立つような
「製餡・菓子・パン業界 週報」を作成してください。

以下の構成にしてください。

【今週の業界週報】

■ 1. 業界全体
重要な動きを3〜5個。

■ 2. 製餡・和菓子
製餡、あんこ、和菓子関連で重要な動き。

■ 3. 菓子業界
新商品、消費者トレンド、原材料など。

■ 4. パン業界
原材料、価格、商品トレンドなど。

■ 5. 原材料価格
小豆、砂糖、小麦、油脂など、
製餡・菓子・パン業界に影響するもの。

■ 6. 松原製餡所への示唆
営業・商品開発・価格設定などについて、
具体的なアドバイスを3つ。

読みやすい日本語で、LINEにそのまま送れる形式にしてください。
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def send_line_message(text):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }

    payload = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    print("LINE status:", response.status_code)
    print(response.text)

    response.raise_for_status()


if __name__ == "__main__":
    report = generate_report()
    send_line_message(report)
