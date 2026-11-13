import re

from fastapi import APIRouter, HTTPException, Request

from templating import BASE_DIR, templates

router = APIRouter()


@router.get("/blog/posts/{post_id}")
async def read_post(request: Request, post_id: str):
    template_path = f"blog/posts/{post_id}.html"
    if not re.fullmatch(r"[a-z0-9-]+", post_id) or not (BASE_DIR / "templates" / template_path).is_file():
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(template_path, {"request": request})


@router.get("/blog")
async def blog_index(request: Request):
    return templates.TemplateResponse("blog/index.html", {"request": request})
