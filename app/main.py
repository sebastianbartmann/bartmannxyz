from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess
from contextlib import asynccontextmanager
from routes import main, blog


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

app.include_router(main.router)
app.include_router(blog.router)
