from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import pages
from app.routers import contact


app = FastAPI()

app.include_router(pages.router)
app.include_router(contact.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# <link rel="stylesheet" href="/static/css/style.css">



