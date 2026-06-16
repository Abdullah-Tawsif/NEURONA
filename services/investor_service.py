import os
import uuid
import shutil

from sqlalchemy.orm import Session
from models.user import User
from models.investor_verification import InvestorVerification



def get_investor_dashboard_data(db: Session, user: dict) -> dict:
    """Gather dashboard context for an investor."""
    investor = db.query(User).filter(User.id == user.get("id")).first()

    if investor and investor.is_verified:
        verified = 1
    else:
        existing = has_existing_verification(db, investor.id if investor else None)
        if existing:
            if existing.status == "rejected":
                verified = 3
            else:
                verified = 2
        else:
            verified = 0

    return {
        "username": user.get("username"),
        "verified": verified,
        "ideas": [],
    }
MANDATORY_FOLDER = "static/uploads/investor_verification/mandatory"
OPTIONAL_FOLDER = "static/uploads/investor_verification/optional"


os.makedirs(MANDATORY_FOLDER, exist_ok=True)
os.makedirs(OPTIONAL_FOLDER, exist_ok=True)


def save_file(upload_file, folder):

    if upload_file is None:
        return None

    ext = os.path.splitext(upload_file.filename)[1]

    filename = f"{uuid.uuid4()}{ext}"

    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return filepath


def create_investor_verification(
    db,
    user_id,
    full_name,
    phone,
    gov_id,
    linkedin_id,
    present_address,
    mandatory_doc,
    optional_doc,
):
    if has_existing_verification(db, user_id) is not None:
        return None

    mandatory_path = save_file(
        mandatory_doc,
        MANDATORY_FOLDER,
    )

    optional_path = save_file(
        optional_doc,
        OPTIONAL_FOLDER,
    )

    verification = InvestorVerification(
        user_id=user_id,
        full_name=full_name,
        phone=phone,
        gov_id=gov_id,
        linkedin_id=linkedin_id,
        present_address=present_address,
        mandatory_doc=mandatory_path,
        optional_doc=optional_path,
        status="pending",
    )

    db.add(verification)
    db.commit()
    db.refresh(verification)

    return verification


def has_existing_verification(db, user_id):
    existing = (
        db.query(InvestorVerification)
        .filter(InvestorVerification.user_id == user_id)
        .first()
    )

    return existing
