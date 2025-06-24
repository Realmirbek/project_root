from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import pages, contact
import os
from fastapi.responses import HTMLResponse
import gettext



app = FastAPI()

app.include_router(pages.router)
app.include_router(contact.router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALES_DIR = os.path.join(BASE_DIR, '..', 'locales')

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

def get_translations(lang: str):
    try:
        translation = gettext.translation('messages', LOCALES_DIR, languages=[lang])
    except FileNotFoundError:
        translation = gettext.NullTranslations()
    return translation.gettext

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, lang: str = 'en'):
    _ = get_translations(lang)
    return templates.TemplateResponse("index.html", {"request": request, "_": _, "lang": lang})


# <link rel="stylesheet" href="/static/css/style.css">

# yodf bcle ihli mpkz



