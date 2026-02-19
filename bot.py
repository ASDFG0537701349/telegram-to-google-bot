import telebot
import os
import io
import json
from flask import Flask
from threading import Thread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# --- שרת קטן כדי ש-Render לא יקרוס ---
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GOOGLE_CREDS_JSON = os.environ.get('GOOGLE_CREDS_JSON')
SPACE_ID = 'spaces/AAQAWoQsWsU'

creds_dict = json.loads(GOOGLE_CREDS_JSON)
creds = service_account.Credentials.from_service_account_info(
    creds_dict, 
    scopes=['https://www.googleapis.com/auth/chat.messages.create']
)
chat_service = build('chat', 'v1', credentials=creds)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['photo', 'text'])
def handle_message(message):
    try:
        if message.text:
            chat_service.spaces().messages().create(
                parent=SPACE_ID,
                body={'text': f"💬 {message.text}"}
            ).execute()
        
        elif message.photo:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            media = MediaIoBaseUpload(io.BytesIO(downloaded_file), mimetype='image/jpeg')
            
            chat_service.spaces().messages().create(
                parent=SPACE_ID,
                body={'text': message.caption if message.caption else "🖼️ תמונה חדשה"},
                media_body=media
            ).execute()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    keep_alive() # מפעיל את השרת ברקע
    print("Bot is running...")
    bot.polling(none_stop=True)
