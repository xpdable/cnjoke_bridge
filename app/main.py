import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI(title="Get a Chuck Norris Jokes :)")

# Use absolute path for static and templates to avoid errors in tests
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Ensure directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

base_random_joke_url = "https://api.chucknorris.io/jokes/random"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    async with httpx.AsyncClient() as client:
        res = await client.get(base_random_joke_url)
        joke = res.json()
    return templates.TemplateResponse("index.html", {"request": request, "joke": joke})

@app.get("/healthz")
async def health():
    return {"status": "ok"}

# TODO with more joke categories
