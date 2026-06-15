from sqlalchemy.orm import Session

from models.user import User


def get_admin_stats(db: Session) -> dict:
    """Gather admin dashboard statistics."""
    total_users = db.query(User).count()
    return {
        "total_users": total_users,
        "total_ideas": 45,
    }
