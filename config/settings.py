import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:5523452@localhost:5432/Neurona",
)

SECRET_KEY = os.getenv("SECRET_KEY", "neurona_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ALLOWED_EMAIL_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "neurona.com",
]

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@neurona.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")
