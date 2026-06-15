from sqlalchemy.orm import Session

from models.user import User


def get_creator_dashboard_data(db: Session, user: dict) -> dict:
    """Gather dashboard context for a creator."""
    creator_name = user.get("username", "Creator")
    creator = db.query(User).filter(User.id == user.get("id")).first()
    verified = creator.is_verified if creator else False
    return {
        "creator_name": creator_name,
        "verified": int(verified),
        "creator_ideas": [],
    }
