# from fastapi import APIRouter, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import RedirectResponse
#
#
# router = APIRouter()
#
# templates = Jinja2Templates(directory="app/templates")
#
# @router.get("/", tags=["Pages"])
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
#
# @router.get("/lang/{lang_code}")
# async def set_language(lang_code: str):
#     if lang_code not in ["ru", "en"]:
#         lang_code = "ru"
#     response = RedirectResponse(url="/")
#     response.set_cookie("lang", lang_code)
#     return response

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import gettext

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Функция получения переводчика
def get_translator(lang: str = "en"):
    return gettext.translation(
        "messages",            # имя файла без расширения .mo
        localedir="locales",   # папка с переводами
        languages=[lang],      # язык
        fallback=True          # не падать при ошибке
    )

# 🌍 Главная страница с поддержкой мультиязычности
@router.get("/", tags=["Pages"])
async def index(request: Request):
    lang = request.cookies.get("lang", "ru")  # по умолчанию русский
    translator = get_translator(lang)
    _ = translator.gettext
    return templates.TemplateResponse("index.html", {"request": request, "_": _})

# 🌐 Смена языка
@router.get("/lang/{lang_code}")
async def set_language(lang_code: str):
    if lang_code not in ["ru", "en"]:
        lang_code = "ru"
    response = RedirectResponse(url="/")
    response.set_cookie("lang", lang_code)
    return response
