from sqlalchemy.orm import Session

from models.user import User


def get_investor_dashboard_data(db: Session, user: dict) -> dict:
    """Gather dashboard context for an investor."""
    investor = db.query(User).filter(User.id == user.get("id")).first()
    verified = investor.is_verified if investor else False
    return {
        "username": user.get("username"),
        "verified": int(verified),
        "ideas": [],
    }
