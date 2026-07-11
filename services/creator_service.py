import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from models.user import User
from models.creator_verification import CreatorVerification
from models.idea import Idea
from models.investment import Investment
from models.idea_extra import IdeaDeleteRequest, IdeaAdminNote


def get_creator_dashboard_data(db: Session, user: dict) -> dict:
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

    # Only show approved/active ideas on dashboard home
    approved_ideas = (
        db.query(Idea)
        .filter(
            Idea.user_id == user.get("id"),
            Idea.is_draft == "false",
            Idea.status == "approved",
        )
        .order_by(Idea.created_at.desc())
        .all()
    )

    active_ideas = []
    for idea in approved_ideas:
        stats = _get_idea_stats(db, idea.id)
        first_image = _safe_first_image(idea.product_images)
        funding_goal = idea.funding_goal or 0
        progress = (stats["total_raised"] / funding_goal * 100) if funding_goal > 0 else 0

        active_ideas.append({
            "id": idea.id,
            "title": idea.title,
            "summary": idea.summary,
            "category": idea.category,
            "funding_goal": funding_goal,
            "currency": idea.currency,
            "equity_offered": idea.equity_offered,
            "equity_sold": stats["equity_sold"],
            "equity_remaining": max(0, idea.equity_offered - stats["equity_sold"]),
            "total_raised": stats["total_raised"],
            "investor_count": stats["investor_count"],
            "progress": round(min(progress, 100), 1),
            "first_image": first_image,
            "product_stage": idea.product_stage,
            "expected_timeline": idea.expected_timeline,
            "revenue_status": idea.revenue_status,
            "created_at": idea.created_at,
        })

    return {
        "creator_name": creator_name,
        "verified": verified,
        "active_ideas": active_ideas,
        "show_verified_popup": show_verified_popup,
    }


def get_creator_ideas_by_status(db: Session, user_id: int) -> dict:
    all_ideas = (
        db.query(Idea)
        .filter(Idea.user_id == user_id, Idea.is_draft == "false")
        .order_by(Idea.created_at.desc())
        .all()
    )

    accepted = []
    under_review = []
    rejected = []

    for idea in all_ideas:
        stats = _get_idea_stats(db, idea.id)
        first_image = _safe_first_image(idea.product_images)
        funding_goal = idea.funding_goal or 0
        progress = (stats["total_raised"] / funding_goal * 100) if funding_goal > 0 else 0

        # Check for pending delete request
        pending_delete = db.query(IdeaDeleteRequest).filter(
            IdeaDeleteRequest.idea_id == idea.id,
            IdeaDeleteRequest.status == "pending",
        ).first()

        # Get admin notes/rejection reason
        rejection_note = db.query(IdeaAdminNote).filter(
            IdeaAdminNote.idea_id == idea.id,
            IdeaAdminNote.note_type.in_(["rejection_reason", "changes_requested"]),
        ).order_by(IdeaAdminNote.created_at.desc()).first()

        card = {
            "id": idea.id,
            "submission_id": idea.submission_id,
            "title": idea.title,
            "summary": idea.summary,
            "category": idea.category,
            "funding_goal": funding_goal,
            "currency": idea.currency,
            "equity_offered": idea.equity_offered,
            "total_raised": stats["total_raised"],
            "investor_count": stats["investor_count"],
            "progress": round(min(progress, 100), 1),
            "first_image": first_image,
            "product_stage": idea.product_stage,
            "status": idea.status,
            "created_at": idea.created_at,
            "has_pending_delete": pending_delete is not None,
            "rejection_note": rejection_note.note if rejection_note else None,
        }

        if idea.status == "approved":
            accepted.append(card)
        elif idea.status in ("submitted", "reviewing"):
            under_review.append(card)
        elif idea.status in ("rejected", "changes_requested"):
            rejected.append(card)

    return {
        "accepted": accepted,
        "under_review": under_review,
        "rejected": rejected,
    }


def create_delete_request(db: Session, idea_id: int, creator_user_id: int, reason: str) -> tuple:
    idea = db.query(Idea).filter(
        Idea.id == idea_id, Idea.user_id == creator_user_id
    ).first()
    if not idea:
        return None, "Idea not found"

    existing = db.query(IdeaDeleteRequest).filter(
        IdeaDeleteRequest.idea_id == idea_id,
        IdeaDeleteRequest.status == "pending",
    ).first()
    if existing:
        return None, "A delete request is already pending for this idea"

    req = IdeaDeleteRequest(
        idea_id=idea_id,
        creator_user_id=creator_user_id,
        reason=reason,
        status="pending",
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req, None


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
    return (
        db.query(CreatorVerification)
        .filter(CreatorVerification.user_id == user_id)
        .first()
    )


def _get_idea_stats(db: Session, idea_id: int) -> dict:
    total_raised = db.query(func.sum(Investment.amount)).filter(
        Investment.idea_id == idea_id,
        Investment.status == "confirmed",
    ).scalar() or 0.0

    investor_count = db.query(func.count(Investment.id)).filter(
        Investment.idea_id == idea_id,
        Investment.status == "confirmed",
    ).scalar() or 0

    equity_sold = db.query(func.sum(Investment.equity_acquired)).filter(
        Investment.idea_id == idea_id,
        Investment.status == "confirmed",
    ).scalar() or 0.0

    return {
        "total_raised": total_raised,
        "investor_count": investor_count,
        "equity_sold": equity_sold,
    }


def _safe_first_image(product_images_json: str) -> str | None:
    if not product_images_json:
        return None
    try:
        imgs = json.loads(product_images_json)
        return imgs[0] if imgs else None
    except Exception:
        return None
