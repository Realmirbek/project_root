from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
import gettext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re



router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Настройки SMTP
SMTP_USER = "mamytalievmirbek2008@gmail.com"
SMTP_PASSWORD = "tnil soau xnri ldzo"  # Замените на актуальный пароль
PHONE_REGEX = r"^0\d{9}$"
EMAIL_REGEX = r"^[\w\.-]+@gmail\.com$"


def get_translator(lang: str = "ru"):
    try:
        return gettext.translation(
            "messages",
            localedir="locales",
            languages=[lang],
            fallback=True
        )
    except:
        return gettext.NullTranslations()


@router.get("/", tags=["Pages"])
async def index(request: Request):
    lang = request.cookies.get("lang", "ru")
    translator = get_translator(lang)
    _ = translator.gettext
    return templates.TemplateResponse("index.html", {
        "request": request,
        "_": _,
        "lang": lang
    })


@router.get("/lang/{lang_code}")
async def set_language(lang_code: str):
    if lang_code not in ["ru", "en"]:
        lang_code = "ru"
    response = RedirectResponse(url="/")
    response.set_cookie("lang", lang_code)
    return response


PHONE_RULES = {
    '+996': {'length': 9, 'pattern': r'^\+996[0-9]{9}$', 'name': 'Кыргызстан'},
    '+7': {'length': 10, 'pattern': r'^\+7[0-9]{10}$', 'name': 'Россия/Казахстан'},
    '+998': {'length': 9, 'pattern': r'^\+998[0-9]{9}$', 'name': 'Узбекистан'}
}


@router.post("/send-message/")
async def send_message(
        request: Request,
        name: str = Form(...),
        email: str = Form(default=""),
        phone: str = Form(...),
        message: str = Form(default="")
):
    # Проверяем AJAX-запрос
    is_ajax = request.headers.get('accept') == 'application/json'

    lang = request.cookies.get("lang", "ru")
    translator = get_translator(lang)
    _ = translator.gettext

    try:
        # Валидация email
        if email and not re.match(EMAIL_REGEX, email):
            if is_ajax:
                return JSONResponse(
                    {"success": False, "message": _("Email must end with @gmail.com")},
                    status_code=400
                )
            raise HTTPException(
                status_code=400,
                detail=_("Email must end with @gmail.com")
            )



        # Валидация телефона
        phone = phone.strip()
        valid = False
        country_name = ""

        for code, rule in PHONE_RULES.items():
            if phone.startswith(code):
                if not re.match(rule['pattern'], phone):
                    if is_ajax:
                        return JSONResponse({
                            "success": False,
                            "message": _("For {country} number must contain {length} digits after {code}").format(
                                country=rule['name'],
                                length=rule['length'],
                                code=code
                            )
                        }, status_code=400)
                    raise HTTPException(
                        status_code=400,
                        detail=_("For {country} number must contain {length} digits after {code}").format(
                            country=rule['name'],
                            length=rule['length'],
                            code=code
                        )
                    )
                valid = True
                country_name = rule['name']
                break

        if not valid:
            supported_countries = ", ".join([rule['name'] for rule in PHONE_RULES.values()])
            if is_ajax:
                return JSONResponse({
                    "success": False,
                    "message": _("Unsupported phone number format. Supported countries: {countries}").format(
                        countries=supported_countries
                    )
                }, status_code=400)
            raise HTTPException(
                status_code=400,
                detail=_("Unsupported phone number format. Supported countries: {countries}").format(
                    countries=supported_countries
                )
            )

        # Форматирование номера
        formatted_phone = phone
        if phone.startswith('+996'):
            formatted_phone = f"+996 {phone[4:7]} {phone[7:9]} {phone[9:]}"
        elif phone.startswith('+7'):
            formatted_phone = f"+7 {phone[2:5]} {phone[5:8]} {phone[8:]}"
        elif phone.startswith('+998'):
            formatted_phone = f"+998 {phone[4:7]} {phone[7:9]} {phone[9:]}"

        # Отправка email
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = SMTP_USER
        msg['Subject'] = _("New message from website")

        body = f"{_('Name')}: {name}\n"
        if email:
            body += f"{_('Email')}: {email}\n"
        body += f"{_('Phone')}: {formatted_phone} ({country_name})"

        if message:
            body += f"\n\n{_('Message')}:\n{message}"

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
        server.quit()

        if is_ajax:
            return JSONResponse({
                "success": True,
                "message": _("Message sent successfully!"),
                "formatted_phone": formatted_phone
            })
        return RedirectResponse(url="/?success=true")

    except Exception as e:
        if is_ajax:
            return JSONResponse({
                "success": False,
                "message": _("Sending error: {error}").format(error=str(e))
            }, status_code=500)
        raise HTTPException(
            status_code=500,
            detail=_("Sending error: {error}").format(error=str(e))
        )

