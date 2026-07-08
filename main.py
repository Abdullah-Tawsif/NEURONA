import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from config.settings import SECRET_KEY
from database.database import engine
from middleware.auth_middleware import RequestLoggingMiddleware
from middleware.error_handlers import register_error_handlers
from models.user import Base
import models.idea  # noqa: F401 — ensure Idea table is registered with Base
from routes.admin import router as admin_router
from routes.auth import router as auth_router
from routes.creator import router as creator_router
from routes.index import router as index_router
from routes.investor import router as investor_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
logger = logging.getLogger("neurona")

app = FastAPI(title="Neurona", docs_url=None, redoc_url=None)

# Middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(RequestLoggingMiddleware)

# Error handlers
register_error_handlers(app)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(creator_router)
app.include_router(investor_router)

# Database init
Base.metadata.create_all(bind=engine)

logger.info("Neurona application started")
