import telebot
import requests
import os

# שליפת הנתונים ממשתני הסביבה (נגדיר אותם ב-Render)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GOOGLE_CHAT_WEBHOOK = os.environ.get('GOOGLE_CHAT_WEBHOOK')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['photo', 'video', 'document', 'text'])
def forward_to_google_chat(message):
    try:
        payload = {}
        
        # טיפול בטקסט
        if message.text:
            payload = {"text": f"💬 *הודעה חדשה:* \n{message.text}"}
        
        # טיפול במדיה (תמונה/וידאו/קובץ)
        else:
            caption = message.caption if message.caption else "נשלחה מדיה חדשה"
            payload = {"text": f"🔔 *{caption}*\n_(הקובץ ממתין לך בטלגרם)_"}

        # שליחה ל-Webhook של גוגל
        if GOOGLE_CHAT_WEBHOOK:
            response = requests.post(GOOGLE_CHAT_WEBHOOK, json=payload)
            if response.status_code == 200:
                print("נשלח לגוגל צ'אט בהצלחה!")
            else:
                print(f"שגיאה מגוגל: {response.status_code}")
        
    except Exception as e:
        print(f"שגיאה בתהליך: {e}")

if __name__ == "__main__":
    print("הבוט עלה לאוויר ומחכה להודעות...")
    bot.polling(none_stop=True)