from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import main, blog, setup
from templating import STATIC_DIR

# No /docs, /redoc or /openapi.json: FastAPI's default doc pages load scripts and fonts
# from third-party CDNs (cdn.jsdelivr.net, fonts.googleapis.com) and this site has no public API.
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(main.router)
app.include_router(blog.router)
app.include_router(setup.router)
