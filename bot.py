import telebot
import requests
import os
import io
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# הגדרות משתני סביבה
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GOOGLE_CHAT_WEBHOOK = os.environ.get('GOOGLE_CHAT_WEBHOOK') # נשמור אותו לגיבוי
GOOGLE_CREDS_JSON = os.environ.get('GOOGLE_CREDS_JSON') # כאן יכנס כל תוכן ה-JSON
SPACE_ID = 'spaces/AAQAWoQsWsU'

# יצירת אישור מהטקסט של ה-JSON
creds_dict = json.loads(GOOGLE_CREDS_JSON)
creds = service_account.Credentials.from_service_account_info(
    creds_dict, 
    scopes=['https://www.googleapis.com/auth/chat.messages.create']
)
chat_service = build('chat', 'v1', credentials=creds)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['photo', 'video', 'document', 'text'])
def handle_message(message):
    try:
        if message.text:
            chat_service.spaces().messages().create(
                parent=SPACE_ID,
                body={'text': f"💬 *הודעה:* {message.text}"}
            ).execute()
        
        elif message.photo:
            # הורדת התמונה מטלגרם
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # העלאה לגוגל
            media_body = MediaIoBaseUpload(io.BytesIO(downloaded_file), mimetype='image/jpeg')
            
            chat_service.spaces().messages().create(
                parent=SPACE_ID,
                body={'text': message.caption if message.caption else "🖼️ נשלחה תמונה"},
                media_body=media_body
            ).execute()
            
        print("נשלח בהצלחה!")
    except Exception as e:
        print(f"שגיאה: {e}")

bot.polling(none_stop=True)
