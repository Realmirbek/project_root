import re
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

# Вставь сюда свой email и пароль от почты (или используй переменные окружения)
SMTP_USER = "mamytalievmirbek2008@gmail.com"
SMTP_PASSWORD = "tnil soau xnri ldzo"

PHONE_REGEX = r"^0\d{9}$"          # Начинается с 0 + 9 цифр = 10 цифр
EMAIL_REGEX = r"^[\w\.-]+@gmail\.com$"

@router.post("/send-message")
async def send_message(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...)
):
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Email должен оканчиваться на @gmail.com")

    if not re.match(PHONE_REGEX, phone):
        raise HTTPException(status_code=400, detail="Телефон должен начинаться с 0 и содержать ровно 10 цифр")

    word_count = len(message.split())
    if word_count > 500:
        raise HTTPException(status_code=400, detail="Сообщение не должно превышать 500 слов")
    # Создание email-сообщения
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER
    msg['Subject'] = "Новое сообщение с сайта"

    body = f"Имя: {name}\nEmail: {email}\nНомер: Телефон: {phone}\nСообщение:\n{message}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
        server.quit()
        return JSONResponse({"success": True, "message":    "Сообщение успешно отправлено!"})
    except Exception as e:
        return JSONResponse({"success": False, "message": f"Ошибка отправки: {e}"})


