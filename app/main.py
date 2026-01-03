from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes import main, blog, config
from pathlib import Path
import os


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

base_dir = Path(__file__).resolve().parent
static_files = [
    base_dir / "static" / "css" / "main.css",
    base_dir / "static" / "css" / "custom.css",
    base_dir / "static" / "scripts" / "htmx.min.js",
]
try:
    static_version = str(
        max(int(p.stat().st_mtime) for p in static_files if p.exists())
    )
except ValueError:
    static_version = os.environ.get("STATIC_VERSION", "1")

templates.env.globals["static_version"] = static_version

app.include_router(main.router)
app.include_router(blog.router)
app.include_router(config.router)
