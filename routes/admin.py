from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from services.idea_service import get_admin_stats
from models.investor_verification import InvestorVerification
from models.creator_verification import CreatorVerification
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ---------------- ADMIN DASHBOARD ----------------
@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")

    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    stats = get_admin_stats(db)

    return templates.TemplateResponse(
        request=request,
        name="admin/admin_dashboard.html",
        context={
            "username": user.get("username", "Admin"),
            **stats,
        },
    )

# ---------------- INVESTOR VERIFICATION PAGE ----------------
@router.get("/admin/admin_verify_investor", response_class=HTMLResponse)
def investor_verifications(
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")

    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    verifications = db.query(InvestorVerification).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/admin_verify_investor.html",
        context={
            "username": user.get("username", "Admin"),
            "verifications": verifications,
        },
    )


# ---------------- APPROVE INVESTOR ----------------
@router.post("/admin/investor/approve/{vid}")
def approve_investor(
    vid: int,
    db: Session = Depends(get_db),
):
    v = db.query(InvestorVerification).filter_by(id=vid).first()

    if v:
        v.status = "approved"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = True
            user.verified_popup_shown = False
        db.commit()

    return RedirectResponse(
        url="/admin/admin_verify_investor",
        status_code=303
    )


# ---------------- REJECT INVESTOR ----------------
@router.post("/admin/investor/reject/{vid}")
def reject_investor(
    vid: int,
    db: Session = Depends(get_db),
):
    v = db.query(InvestorVerification).filter_by(id=vid).first()

    if v:
        v.status = "rejected"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = False
            user.verified_popup_shown = False
        db.commit()

    return RedirectResponse(
        url="/admin/admin_verify_investor",
        status_code=303
    )


# ---------------- CREATOR VERIFICATION PAGE ----------------
@router.get("/admin/admin_verify_creator", response_class=HTMLResponse)
def creator_verifications(
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")

    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    verifications = db.query(CreatorVerification).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/admin_verify_creator.html",
        context={
            "username": user.get("username", "Admin"),
            "verifications": verifications,
        },
    )


# ---------------- APPROVE CREATOR ----------------
@router.post("/admin/creator/approve/{vid}")
def approve_creator(
    vid: int,
    db: Session = Depends(get_db),
):
    v = db.query(CreatorVerification).filter_by(id=vid).first()

    if v:
        v.status = "approved"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = True
            user.verified_popup_shown = False
        db.commit()

    return RedirectResponse(
        url="/admin/admin_verify_creator",
        status_code=303
    )


# ---------------- REJECT CREATOR ----------------
@router.post("/admin/creator/reject/{vid}")
def reject_creator(
    vid: int,
    db: Session = Depends(get_db),
):
    v = db.query(CreatorVerification).filter_by(id=vid).first()

    if v:
        v.status = "rejected"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = False
            user.verified_popup_shown = False
        db.commit()

    return RedirectResponse(
        url="/admin/admin_verify_creator",
        status_code=303
    )
