from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import httpx

app = FastAPI(title="Get a Chunk Norris Jokes :)")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
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

#TODO with more joke categories