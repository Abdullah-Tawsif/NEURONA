from sqlalchemy.orm import Session

from config.settings import ADMIN_EMAIL, ADMIN_PASSWORD
from models.user import User
from utils.security import hash_password, verify_password
from utils.validators import is_email_domain_allowed


def register_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    role: str,
) -> tuple[User | None, str | None]:
    """Create a new user. Returns (user, error_message)."""

    if not is_email_domain_allowed(email):
        return None, "Email domain not allowed"

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None, "Email already registered"

    user = User(
        username=username,
        email=email,
        password=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, None


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> dict | None:
    """Return session dict on success, None on failure."""

    # Admin shortcut
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return {"email": email, "role": "admin"}

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
