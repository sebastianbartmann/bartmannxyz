from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        subprocess.run([
            "tailwindcss",
            "-i",
            "./static/tailwind.css",
            "-o",
            "./static/css/main.css",
            "--minify"
        ])
    except Exception as e:
        print(f"Error running tailwindcss: {e}")

    yield


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/blog")
async def read_root(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})


@app.get("/blog/posts/how-it-started")
async def read_root(request: Request):
    return templates.TemplateResponse("posts/how-it-started.html", {"request": request})

@app.get("/projects")
async def read_root(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})


# Serve robots.txt and sitemap.xml directly
@app.get("/robots.txt")
async def robots_txt():
    return StaticFiles(directory="static").lookup_path("/robots.txt")


@app.get("/sitemap.xml")
async def sitemap_xml():
    return StaticFiles(directory="static").lookup_path("/sitemap.xml")
