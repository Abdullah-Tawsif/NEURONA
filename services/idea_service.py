from sqlalchemy import func
from sqlalchemy.orm import Session

from models.user import User
from models.creator_verification import CreatorVerification
from models.investor_verification import InvestorVerification


def get_admin_stats(db: Session) -> dict:
    """Gather admin dashboard statistics."""
    # Total users
    total_users = db.query(User).count()

    # Users by role
    total_creators = db.query(User).filter(User.role == "creator").count()
    total_investors = db.query(User).filter(User.role == "investor").count()

    # Verified users
    total_verified = db.query(User).filter(User.is_verified == True).count()

    # Pending verifications
    pending_creator_verifications = db.query(CreatorVerification).filter(
        CreatorVerification.status == "pending"
    ).count()

    pending_investor_verifications = db.query(InvestorVerification).filter(
        InvestorVerification.status == "pending"
    ).count()

    total_pending_verifications = pending_creator_verifications + pending_investor_verifications

    # Active users (simplified - users who are active)
    active_users = db.query(User).filter(User.is_active == True).count()

    creator_percent = (total_creators / total_users * 100) if total_users else 0
    investor_percent = (total_investors / total_users * 100) if total_users else 0
    verified_percent = (total_verified / total_users * 100) if total_users else 0

    return {
        "total_users": total_users,
        "total_creators": total_creators,
        "total_investors": total_investors,
        "total_verified": total_verified,
        "pending_creator_verifications": pending_creator_verifications,
        "pending_investor_verifications": pending_investor_verifications,
        "total_pending_verifications": total_pending_verifications,
        "active_users": active_users,
        "total_ideas": 45,  # Placeholder until ideas table is implemented
        "creator_percent": creator_percent,
        "investor_percent": investor_percent,
        "verified_percent": verified_percent,
    }
