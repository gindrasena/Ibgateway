
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import Base, engine
from .routes.ui import router as ui_router
from .routes.api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    Base.metadata.create_all(bind=engine)
    app.include_router(ui_router)
    app.include_router(api_router)
    app.mount('/static', StaticFiles(directory='static'), name='static')
    return app


app = create_app()
