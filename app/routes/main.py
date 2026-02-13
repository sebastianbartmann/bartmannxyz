from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/projects")
async def read_root(request: Request):
    return templates.TemplateResponse("/projects/index.html", {"request": request})


@router.get("/projects/nostr-client/project-index")
async def read_root(request: Request):
    return templates.TemplateResponse("/projects/nostr-client/project-index.html", {"request": request})


@router.get("/projects/apartment-prices-vienna/project-index")
async def read_root(request: Request):
    return templates.TemplateResponse("/projects/apartment-prices-vienna/project-index.html", {"request": request})


# Serve robots.txt and sitemap.xml directly
@router.get("/robots.txt")
async def robots_txt():
    return StaticFiles(directory="static").lookup_path("/robots.txt")


@router.get("/sitemap.xml")
async def sitemap_xml():
    return StaticFiles(directory="static").lookup_path("/sitemap.xml")
