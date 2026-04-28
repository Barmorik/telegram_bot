from fastapi import FastAPI, Request
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = FastAPI()


def send_message(chat_id: int, text: str):
    url = f"{TELEGRAM_API}/sendMessage"
    try:
        r = requests.post(
            url,
            json={"chat_id": chat_id, "text": text},
            timeout=10
        )
        print("SEND:", r.status_code, r.text)
    except Exception as e:
        print("ERROR SEND:", e)


def process_message(text: str) -> str:
    if text == "/start":
        return "Привет! Я твой Telegram-бот на Python + FastAPI."

    if text.lower() == "/run":
        return "Запускаю стратегию..."

    return f"Ты написал: {text}"


@app.get("/")
def home():
    return {"message": "FastAPI сервер работает"}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        print("DATA:", data)

        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if chat_id and text:
            answer = process_message(text)
            send_message(chat_id, answer)

        return {"ok": True}

    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return {"ok": True}
# def main():
#     pass
#
# if __name__ == "__main__":
#     main()
