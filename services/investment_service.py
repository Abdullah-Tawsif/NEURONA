from sqlalchemy.orm import Session
from sqlalchemy import func

from models.investment import Investment
from models.bookmark import Bookmark
from models.idea import Idea
from models.user import User


def get_idea_investment_stats(db: Session, idea_id: int) -> dict:
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


def get_investor_stats(db: Session, investor_user_id: int) -> dict:
    total_invested = db.query(func.sum(Investment.amount)).filter(
        Investment.investor_user_id == investor_user_id,
        Investment.status == "confirmed",
    ).scalar() or 0.0

    active_investments = db.query(func.count(func.distinct(Investment.idea_id))).filter(
        Investment.investor_user_id == investor_user_id,
        Investment.status == "confirmed",
    ).scalar() or 0

    return {
        "total_invested": total_invested,
        "active_investments": active_investments,
    }


def get_total_available_ideas(db: Session) -> int:
    return db.query(func.count(Idea.id)).filter(
        Idea.status == "approved",
        Idea.is_draft == "false",
    ).scalar() or 0


def get_approved_ideas_for_investor(db: Session, investor_user_id: int) -> list:
    ideas = db.query(Idea).filter(
        Idea.status == "approved",
        Idea.is_draft == "false",
    ).order_by(Idea.created_at.desc()).all()

    bookmarked_ids = set()
    if investor_user_id:
        bookmarks = db.query(Bookmark.idea_id).filter(
            Bookmark.investor_user_id == investor_user_id
        ).all()
        bookmarked_ids = {b.idea_id for b in bookmarks}

    result = []
    for idea in ideas:
        stats = get_idea_investment_stats(db, idea.id)
        creator = db.query(User).filter(User.id == idea.user_id).first()

        import json as _json

        def safe_first_image(val):
            if not val:
                return None
            try:
                imgs = _json.loads(val)
                return imgs[0] if imgs else None
            except Exception:
                return None

        def safe_first_founder(val):
            if not val:
                return {}
            try:
                founders = _json.loads(val)
                return founders[0] if founders else {}
            except Exception:
                return {}

        funding_goal = idea.funding_goal or 0
        progress = (stats["total_raised"] / funding_goal * 100) if funding_goal > 0 else 0

        result.append({
            "id": idea.id,
            "submission_id": idea.submission_id,
            "title": idea.title,
            "category": idea.category,
            "summary": idea.summary,
            "funding_goal": funding_goal,
            "currency": idea.currency,
            "equity_offered": idea.equity_offered,
            "product_stage": idea.product_stage,
            "expected_timeline": idea.expected_timeline,
            "total_raised": stats["total_raised"],
            "investor_count": stats["investor_count"],
            "equity_sold": stats["equity_sold"],
            "progress": round(min(progress, 100), 1),
            "first_image": safe_first_image(idea.product_images),
            "creator_name": idea.full_name or (creator.username if creator else ""),
            "first_founder": safe_first_founder(idea.founders),
            "is_bookmarked": idea.id in bookmarked_ids,
            "created_at": idea.created_at,
        })

    return result


def toggle_bookmark(db: Session, idea_id: int, investor_user_id: int) -> bool:
    existing = db.query(Bookmark).filter(
        Bookmark.idea_id == idea_id,
        Bookmark.investor_user_id == investor_user_id,
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return False
    else:
        bookmark = Bookmark(idea_id=idea_id, investor_user_id=investor_user_id)
        db.add(bookmark)
        db.commit()
        return True


def is_bookmarked(db: Session, idea_id: int, investor_user_id: int) -> bool:
    return db.query(Bookmark).filter(
        Bookmark.idea_id == idea_id,
        Bookmark.investor_user_id == investor_user_id,
    ).first() is not None
