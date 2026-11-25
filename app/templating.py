"""The one Jinja environment for all routes, with the globals every page needs."""
from datetime import date
from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Cache-busting query value for the stylesheets, scripts and bounce images: newest modification time.
_versioned = [
    *sorted((STATIC_DIR / "css").glob("*.css")),
    STATIC_DIR / "scripts" / "theme.js",
    STATIC_DIR / "scripts" / "bounce.js",
    *sorted((STATIC_DIR / "images" / "bartmann").glob("*.png")),
]
templates.env.globals["static_version"] = str(max(int(p.stat().st_mtime) for p in _versioned))
templates.env.globals["current_year"] = lambda: date.today().year
