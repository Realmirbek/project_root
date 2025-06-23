from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

# Вставь сюда свой email и пароль от почты (или используй переменные окружения)
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_email_password"

@router.post("/send-message")
async def send_message(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Создание email-сообщения
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER
    msg['Subject'] = "Новое сообщение с сайта"

    body = f"Имя: {name}\nEmail: {email}\nСообщение:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
        server.quit()
        return JSONResponse({"success": True, "message": "Сообщение успешно отправлено!"})
    except Exception as e:
        return JSONResponse({"success": False, "message": f"Ошибка отправки: {e}"})


# п т с у з б ч б е н ч к а у й в