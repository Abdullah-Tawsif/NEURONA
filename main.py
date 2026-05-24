from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.auth import router as auth_router
from routes.index import router as index_router
from routes.admin import router as admin_router


app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(admin_router)
