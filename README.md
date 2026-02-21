# telegram-to-google-bot

בוט שמעביר הודעות (טקסט + תמונות) מטלגרם לגוגל צ'אט, באופן אוטומטי.

---

## מה הבוט עושה?

כל הודעה שנשלחת לבוט בטלגרם (או בקבוצה שהבוט חבר בה) מועברת אוטומטית ל-Google Chat Space:

- **טקסט** - נשלח כהודעת טקסט רגילה
- **תמונות** - נשלחות ככרטיס עם תצוגה מקדימה של התמונה

---

## דרישות מוקדמות

- חשבון טלגרם
- חשבון Google Workspace (עסקי - לא חשבון Gmail רגיל)
- חשבון ב-Render (חינם)
- חשבון GitHub

---

## שלב 1: יצירת בוט בטלגרם

### 1.1 פתיחת BotFather

1. פתחו את **טלגרם** (אפליקציה או דפדפן)
2. בשורת החיפוש, חפשו **`BotFather`**
3. בחרו את החשבון הרשמי (עם סימן אימות כחול)
4. לחצו **Start**

### 1.2 יצירת הבוט

1. שלחו את ההודעה: `/newbot`
2. BotFather ישאל איך לקרוא לבוט - הקלידו שם (לדוגמה: `My Forwarding Bot`)
3. BotFather ישאל על username - הקלידו שם שמסתיים ב-`bot` (לדוגמה: `my_forwarding_bot`)
4. תקבלו הודעה עם **Token** שנראה ככה:
   ```
   123456789:ABCdefGHIjklmnoPQRstuvWXYZ-abcdefGH
   ```

**שמרו את ה-Token!** הוא סודי ומשמש לאימות הבוט. זה ה-`TELEGRAM_TOKEN` שתצטרכו בהמשך.

### 1.3 הוספת הבוט לקבוצה (אופציונלי)

אם רוצים שהבוט יעביר הודעות מקבוצת טלגרם:

1. פתחו את הקבוצה בטלגרם
2. לחצו על שם הקבוצה למעלה
3. לחצו **Add Members**
4. חפשו את ה-username של הבוט שיצרתם
5. הוסיפו אותו לקבוצה

---

## שלב 2: יצירת Webhook בגוגל צ'אט

### 2.1 יצירת Space בגוגל צ'אט

1. פתחו את **Google Chat** בדפדפן: https://chat.google.com
2. בתפריט השמאלי, מצאו את **Spaces**
3. לחצו על **+** (New chat) ואז **Create a space**
4. תנו שם ל-Space (לדוגמה: `Bot Notifications`)
5. לחצו **Create**

### 2.2 יצירת Webhook

1. פתחו את ה-Space שיצרתם
2. לחצו על **החץ למטה** ליד שם ה-Space (או שלוש נקודות)
3. בחרו **Apps & integrations**
4. לחצו **Add webhooks**
5. הגדירו:
   - **Name**: שם ל-webhook (לדוגמה: `Telegram Bot`)
   - **Avatar URL**: אופציונלי - כתובת תמונה לאייקון
6. לחצו **Save**

### 2.3 העתקת כתובת ה-Webhook

1. אחרי השמירה, ה-webhook יופיע ברשימה
2. לחצו על **שלוש נקודות** ליד ה-webhook
3. בחרו **Copy link**

הכתובת תיראה ככה:
```
https://chat.googleapis.com/v1/spaces/ABC123/messages?key=xyz&token=abc
```

**שמרו את הכתובת!** זה ה-`GOOGLE_CHAT_WEBHOOK` שתצטרכו בהמשך.

---

## שלב 3: העלאת הקוד ל-GitHub

### 3.1 יצירת Repository

1. היכנסו ל-GitHub: https://github.com
2. לחצו **+** (למעלה מימין) ואז **New repository**
3. תנו שם (לדוגמה: `telegram-to-google-bot`)
4. בחרו **Private**
5. לחצו **Create repository**

### 3.2 העלאת הקוד

אם עדיין לא עשיתם clone:

```bash
git clone https://github.com/YOUR_USERNAME/telegram-to-google-bot.git
cd telegram-to-google-bot
```

העתיקו את כל קבצי הפרויקט לתיקייה ועשו push:

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

---

## שלב 4: הגדרת Render (דיפלוי)

### 4.1 יצירת חשבון

1. היכנסו ל: https://render.com
2. לחצו **Get Started for Free**
3. הירשמו עם חשבון GitHub (הכי קל)

### 4.2 יצירת שירות חדש

1. בדשבורד של Render, לחצו **New +**
2. בחרו **Web Service**
3. חברו את חשבון ה-GitHub שלכם (אם עדיין לא מחובר)
4. מצאו את ה-repository ולחצו **Connect**

### 4.3 הגדרות השירות

מלאו את הפרטים הבאים:

| שדה | ערך |
|-----|------|
| **Name** | `telegram-to-google-bot` (או כל שם אחר) |
| **Region** | `Frankfurt (EU Central)` (הכי קרוב לישראל) |
| **Branch** | `main` |
| **Build Command** | `pip install .` |
| **Start Command** | `python -m src.main` |
| **Instance Type** | Free |

### 4.4 הגדרת משתני סביבה (Environment Variables)

זה החלק הכי חשוב! גללו למטה לאזור **Environment Variables** ולחצו **Add Environment Variable** עבור כל אחד:

| Key | Value |
|-----|-------|
| `TELEGRAM_TOKEN` | ה-Token שקיבלתם מ-BotFather |
| `GOOGLE_CHAT_WEBHOOK` | כתובת ה-Webhook שהעתקתם מגוגל צ'אט |
| `LOG_LEVEL` | `INFO` |
| `PYTHON_VERSION` | `3.12.0` |

### 4.5 יצירה והפעלה

1. לחצו **Create Web Service**
2. Render יתחיל לבנות ולהפעיל את הבוט
3. עקבו אחרי הלוגים - כשתראו `Bot started, entering polling loop` הבוט עובד

---

## שלב 5: בדיקה

1. פתחו את הבוט בטלגרם (חפשו את ה-username שנתתם)
2. שלחו לו הודעת טקסט
3. בדקו שההודעה הגיעה ל-Google Chat Space
4. שלחו תמונה
5. בדקו שהתמונה מופיעה בגוגל צ'אט ככרטיס

---

## פיתוח מקומי

### התקנה

```bash
git clone https://github.com/YOUR_USERNAME/telegram-to-google-bot.git
cd telegram-to-google-bot
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### הגדרת משתני סביבה

```bash
cp .env.example .env
```

ערכו את `.env` עם הערכים שלכם:
```
TELEGRAM_TOKEN=your-token-here
GOOGLE_CHAT_WEBHOOK=your-webhook-url-here
```

### הרצה מקומית

```bash
python -m src.main
```

### טסטים

```bash
# הרצת כל הטסטים
pytest

# עם דוח כיסוי
pytest --cov=src --cov-report=term-missing
```

### Linting

```bash
ruff check src/ tests/
```

---

## משתני סביבה

| משתנה | חובה | ברירת מחדל | תיאור |
|-------|------|------------|-------|
| `TELEGRAM_TOKEN` | כן | - | טוקן מ-BotFather |
| `GOOGLE_CHAT_WEBHOOK` | כן | - | כתובת Webhook של גוגל צ'אט |
| `PORT` | לא | `5000` | פורט שרת Health Check |
| `LOG_LEVEL` | לא | `INFO` | רמת לוגים (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |

---

## מבנה הפרויקט

```
src/
  main.py                              # נקודת כניסה ראשית
  config/
    settings.py                        # הגדרות (Pydantic Settings)
    logging_config.py                  # הגדרת לוגים
  models/
    message.py                         # מודלים: ForwardableMessage, PhotoData
  exceptions/
    base.py                            # שגיאת בסיס
    telegram_errors.py                 # שגיאות טלגרם
    google_chat_errors.py              # שגיאות גוגל צ'אט
  clients/
    interfaces.py                      # ממשקים מופשטים
    telegram_client.py                 # לקוח טלגרם
    google_chat_webhook_client.py      # לקוח גוגל צ'אט (webhook)
  services/
    forwarder.py                       # לוגיקה עסקית
  handlers/
    message_handler.py                 # טיפול בהודעות טלגרם
  server/
    health_server.py                   # שרת Health Check ל-Render
tests/
  unit/                                # טסטים יחידתיים
  integration/                         # טסטים אינטגרטיביים
  e2e/                                 # טסטים מקצה לקצה
```

---

## פתרון בעיות

### הבוט לא מגיב
- בדקו שה-`TELEGRAM_TOKEN` נכון
- בדקו בלוגים של Render שאין שגיאות
- ודאו שהבוט רץ (סטטוס `Live` ב-Render)

### טקסט עובר אבל תמונות לא
- בדקו שה-`GOOGLE_CHAT_WEBHOOK` נכון ותקין
- ודאו שה-Space בגוגל צ'אט עדיין קיים
- בדקו בלוגים אם יש שגיאות webhook

### הבוט נכבה אחרי כמה דקות
- בתוכנית החינמית של Render, השירות נכבה אחרי 15 דקות של חוסר פעילות
- שדרגו לתוכנית בתשלום ($7/חודש) לשירות רציף
- לחלופין, השתמשו בשירות חיצוני שעושה ping כל כמה דקות (כמו UptimeRobot)

### שגיאת `ValidationError` בהפעלה
- חסר משתנה סביבה נדרש
- בדקו שהגדרתם את `TELEGRAM_TOKEN` ו-`GOOGLE_CHAT_WEBHOOK`
