from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware


from routes.auth import router as auth_router
from routes.index import router as index_router
from routes.admin import router as admin_router
from routes.creator import router as creator_router
from routes import auth, admin, creator, index

from database.database import engine
from models.user import User

app = FastAPI()

# SESSION MIDDLEWARE
app.add_middleware(
    SessionMiddleware,
    secret_key="neurona_secret_key"
)

# Static files 
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(creator_router)

#database
User.metadata.create_all(bind=engine)
