import telebot
import os
import requests
import json
import io
from flask import Flask
from threading import Thread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Flask('')
@app.route('/')
def home(): return "OK"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
def keep_alive(): Thread(target=run).start()

# משתני סביבה מ-Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GOOGLE_CHAT_WEBHOOK = os.environ.get('GOOGLE_CHAT_WEBHOOK')
GOOGLE_CREDS_JSON = os.environ.get('GOOGLE_CREDS_JSON')
SPACE_ID = os.environ.get('SPACE_ID') # צריך להיות spaces/AAAA...

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# הגדרת הרשאות גוגל לתמונות
creds_dict = json.loads(GOOGLE_CREDS_JSON)
creds = service_account.Credentials.from_service_account_info(
    creds_dict, scopes=['https://www.googleapis.com/auth/chat.messages.create']
)
chat_service = build('chat', 'v1', credentials=creds)

@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    try:
        if message.text:
            # שליחת טקסט דרך Webhook (פשוט ומהיר)
            requests.post(GOOGLE_CHAT_WEBHOOK, json={'text': message.text})
        
        elif message.photo:
            # הורדת התמונה מטלגרם
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # העלאה לגוגל צ'אט דרך ה-API (בשביל תמונות חייבים API)
            media = MediaIoBaseUpload(io.BytesIO(downloaded_file), mimetype='image/jpeg')
            chat_service.spaces().messages().create(
                parent=SPACE_ID,
                body={'text': message.caption if message.caption else "🖼️ תמונה"},
                media_body=media
            ).execute()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
