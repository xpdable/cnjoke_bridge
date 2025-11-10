import os
import re
import urllib.parse
import html

from fastapi import FastAPI, Request, Query
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
BASE_API = "https://api.chucknorris.io/jokes"

MAX_QUERY_LEN = 120
MIN_QUERY_LEN = 3
QUERY_ALLOWED_RE = re.compile(r"^[\w\-\.\,\s]{1,%d}$" % MAX_QUERY_LEN)

# Default get one random joke
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    async with httpx.AsyncClient() as client:
        res = await client.get(base_random_joke_url)
        joke = res.json()
        print(type(joke))
    return templates.TemplateResponse("index.html", {"request": request, "joke": joke})

# Health Check
@app.get("/healthz")
async def health():
    return {"status": "ok"}

# Fetch for all categories
async def fetch_categories_safe():
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{BASE_API}/categories")
        r.raise_for_status()
        return r.json()

# Fetch jokes by category
@app.get("/category", response_class=HTMLResponse)
async def category_view(request: Request, category: str | None = Query(default="")):
    # get all categories dropdown
    try:
        categories = await fetch_categories_safe()
    except Exception:
        categories = []

    selected = category or ""
    selected_joke = None
    if category:
        if category in categories:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{BASE_API}/random", params={"category": category})
                if r.status_code == 200:
                    selected_joke = r.json()
        else:
            selected_joke = None

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "joke": None,
            "categories": categories,
            "selected_category": selected,
            "query": "",
            "search_results": None,
            "category_joke": selected_joke,
        },
    )

@app.get("/search", response_class=HTMLResponse)
async def search_view(request: Request, query: str | None = Query(default="")):
    try:
        categories = await fetch_categories_safe()
    except Exception:
        categories = []

    q = (query or "").strip()
    safe_q = html.escape(q)
    search_results = None
    error_msg = ""

    if q:
        if len(q) > MAX_QUERY_LEN or len(q) < MIN_QUERY_LEN or not QUERY_ALLOWED_RE.match(q):
            error_msg = error_msg = (
                f"Invalid search query. Allowed: letters, numbers, spaces and -_., "
                f"length must be between {MIN_QUERY_LEN} and {MAX_QUERY_LEN} characters."
            )
            search_results = {"total": 0, "result": []}
        else:
            async with httpx.AsyncClient(timeout=8.0) as client:
                r = await client.get(f"{BASE_API}/search", params={"query": q})
                if r.status_code == 200:
                    search_results = r.json()
                else:
                    search_results = {"total": 0, "result": []}
    else:
        error_msg = "Please enter a search text."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "joke": None,
            "categories": categories,
            "selected_category": "",
            "query": safe_q,
            "search_results": search_results,
            "error_msg": error_msg,
            "category_joke": None,
        },
    )