from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/blog/posts/{post_id}")
async def read_blog(request: Request, post_id: str):
    template_path = f"blog/posts/{post_id}.html"
    full_template_path = os.path.join("templates", template_path)

    if not os.path.exists(full_template_path):
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(template_path, {"request": request})


@router.get("/blog")
async def read_root(request: Request):
    return templates.TemplateResponse("blog/index.html", {"request": request})
