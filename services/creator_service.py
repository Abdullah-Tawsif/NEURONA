from sqlalchemy.orm import Session
from models.user import User
from models.creator_verification import CreatorVerification


def get_creator_dashboard_data(db: Session, user: dict) -> dict:
    """Gather dashboard context for a creator."""
    creator_name = user.get("username", "Creator")
    creator = db.query(User).filter(User.id == user.get("id")).first()

    if creator and creator.is_verified:
        verified = 1
        show_verified_popup = not creator.verified_popup_shown
    else:
        existing = has_existing_verification(db, creator.id if creator else None)
        if existing:
            if existing.status == "rejected":
                verified = 3
            else:
                verified = 2
        else:
            verified = 0
        show_verified_popup = False

    return {
        "creator_name": creator_name,
        "verified": verified,
        "creator_ideas": [],
        "show_verified_popup": show_verified_popup,
    }


def create_creator_verification(
    db,
    user_id,
    full_name,
    phone,
    gov_id,
    linkedin_id,
    present_address,
):
    existing = has_existing_verification(db, user_id)

    if existing:
        if existing.status == "pending":
            return None
        existing.full_name = full_name
        existing.phone = phone
        existing.gov_id = gov_id
        existing.linkedin_id = linkedin_id
        existing.present_address = present_address
        existing.status = "pending"
        db.commit()
        db.refresh(existing)
        return existing

    verification = CreatorVerification(
        user_id=user_id,
        full_name=full_name,
        phone=phone,
        gov_id=gov_id,
        linkedin_id=linkedin_id,
        present_address=present_address,
        status="pending",
    )

    db.add(verification)
    db.commit()
    db.refresh(verification)

    return verification


def has_existing_verification(db, user_id):
    existing = (
        db.query(CreatorVerification)
        .filter(CreatorVerification.user_id == user_id)
        .first()
    )

    return existing
