from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routes.auth import router as auth_router
from routes.index import router as index_router
from routes.admin import router as admin_router
from routes.creator import router as creator_router
from routes.investor import router as investor_router

from database.database import engine
from models.user import Base  # IMPORTANT FIX

app = FastAPI()

# ======================
# SESSION MIDDLEWARE
# ======================
app.add_middleware(
    SessionMiddleware,
    secret_key="neurona_secret_key"
)

# ======================
# STATIC FILES
# ======================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ======================
# ROUTERS
# ======================
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(creator_router)
app.include_router(investor_router)

# ======================
# DATABASE INIT
# ======================
Base.metadata.create_all(bind=engine)
