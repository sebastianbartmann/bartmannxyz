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


@router.get("/favicon.ico")
async def favicon():
    return FileResponse(STATIC_DIR / "favicon.svg", media_type="image/svg+xml")
