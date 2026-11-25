from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from templating import STATIC_DIR, templates

router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/projects")
async def projects(request: Request):
    return templates.TemplateResponse("projects/index.html", {"request": request})


@router.get("/privacy")
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})


@router.get("/robots.txt")
async def robots_txt():
    return FileResponse(STATIC_DIR / "robots.txt", media_type="text/plain")


@router.get("/sitemap.xml")
async def sitemap_xml():
    return FileResponse(STATIC_DIR / "sitemap.xml", media_type="application/xml")


# Tab icon at the root paths browsers and iOS request on their own.
@router.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    return FileResponse(STATIC_DIR / "favicon.ico", media_type="image/x-icon")


@router.get("/favicon.svg", include_in_schema=False)
async def favicon_svg():
    return FileResponse(STATIC_DIR / "favicon.svg", media_type="image/svg+xml")


@router.get("/apple-touch-icon.png", include_in_schema=False)
async def apple_touch_icon():
    return FileResponse(STATIC_DIR / "apple-touch-icon.png", media_type="image/png")
