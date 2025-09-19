from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse
import os
from pathlib import Path

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


# SSH Keys endpoints
@router.get("/ssh/keys", response_class=PlainTextResponse)
async def list_ssh_keys():
    ssh_keys_dir = Path(__file__).parent.parent / "ssh_keys"
    if not ssh_keys_dir.exists():
        raise HTTPException(status_code=404, detail="SSH keys directory not found")
    
    keys = [f.stem for f in ssh_keys_dir.glob("*.pub")]
    return "\n".join(keys)


@router.get("/ssh/keys/all", response_class=PlainTextResponse)
async def get_all_ssh_keys():
    ssh_keys_dir = Path(__file__).parent.parent / "ssh_keys"
    if not ssh_keys_dir.exists():
        raise HTTPException(status_code=404, detail="SSH keys directory not found")
    
    all_keys = []
    for key_file in ssh_keys_dir.glob("*.pub"):
        all_keys.append(key_file.read_text().strip())
    
    return "\n".join(all_keys)


@router.get("/ssh/keys/{key_name}", response_class=PlainTextResponse)
async def get_ssh_key(key_name: str):
    ssh_keys_dir = Path(__file__).parent.parent / "ssh_keys"
    key_file = ssh_keys_dir / f"{key_name}.pub"
    
    if not key_file.exists():
        raise HTTPException(status_code=404, detail=f"SSH key '{key_name}' not found")
    
    return key_file.read_text().strip()
