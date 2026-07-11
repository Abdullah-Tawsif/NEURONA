from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from services.idea_service import get_admin_stats, get_all_ideas
from models.investor_verification import InvestorVerification
from models.creator_verification import CreatorVerification
from models.user import User
from models.idea import Idea
from models.idea_extra import IdeaDeleteRequest, IdeaAdminNote

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ---------------- ADMIN DASHBOARD ----------------
@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)
    stats = get_admin_stats(db)
    return templates.TemplateResponse(
        request=request,
        name="admin/admin_dashboard.html",
        context={"username": user.get("username", "Admin"), **stats},
    )


# ---------------- INVESTOR VERIFICATION ----------------
@router.get("/admin/admin_verify_investor", response_class=HTMLResponse)
def investor_verifications(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)
    stats = get_admin_stats(db)
    verifications = db.query(InvestorVerification).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/admin_verify_investor.html",
        context={"username": user.get("username", "Admin"), "verifications": verifications, **stats},
    )


@router.post("/admin/investor/approve/{vid}")
def approve_investor(vid: int, db: Session = Depends(get_db)):
    v = db.query(InvestorVerification).filter_by(id=vid).first()
    if v:
        v.status = "approved"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = True
            user.verified_popup_shown = False
        db.commit()
    return RedirectResponse(url="/admin/admin_verify_investor", status_code=303)


@router.post("/admin/investor/reject/{vid}")
def reject_investor(vid: int, db: Session = Depends(get_db)):
    v = db.query(InvestorVerification).filter_by(id=vid).first()
    if v:
        v.status = "rejected"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = False
            user.verified_popup_shown = False
        db.commit()
    return RedirectResponse(url="/admin/admin_verify_investor", status_code=303)


# ---------------- CREATOR VERIFICATION ----------------
@router.get("/admin/admin_verify_creator", response_class=HTMLResponse)
def creator_verifications(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)
    stats = get_admin_stats(db)
    verifications = db.query(CreatorVerification).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/admin_verify_creator.html",
        context={"username": user.get("username", "Admin"), "verifications": verifications, **stats},
    )


@router.post("/admin/creator/approve/{vid}")
def approve_creator(vid: int, db: Session = Depends(get_db)):
    v = db.query(CreatorVerification).filter_by(id=vid).first()
    if v:
        v.status = "approved"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = True
            user.verified_popup_shown = False
        db.commit()
    return RedirectResponse(url="/admin/admin_verify_creator", status_code=303)


@router.post("/admin/creator/reject/{vid}")
def reject_creator(vid: int, db: Session = Depends(get_db)):
    v = db.query(CreatorVerification).filter_by(id=vid).first()
    if v:
        v.status = "rejected"
        user = db.query(User).filter(User.id == v.user_id).first()
        if user:
            user.is_verified = False
            user.verified_popup_shown = False
        db.commit()
    return RedirectResponse(url="/admin/admin_verify_creator", status_code=303)


# ---------------- ADMIN IDEAS PAGE ----------------
@router.get("/admin_ideas", response_class=HTMLResponse)
def admin_ideas(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)
    stats = get_admin_stats(db)
    ideas = get_all_ideas(db)

    idea_list = []
    for idea in ideas:
        creator = db.query(User).filter(User.id == idea.user_id).first()
        idea_list.append({
            "id": idea.id,
            "submission_id": idea.submission_id,
            "title": idea.title,
            "category": idea.category,
            "funding_goal": idea.funding_goal,
            "currency": idea.currency,
            "equity_offered": idea.equity_offered,
            "product_stage": idea.product_stage,
            "status": idea.status,
            "is_draft": idea.is_draft,
            "created_at": idea.created_at,
            "creator_name": creator.username if creator else "Unknown",
            "creator_email": creator.email if creator else "",
        })
    idea_list = [i for i in idea_list if i["is_draft"] != "true"]

    # Pending delete requests count
    pending_deletes = db.query(IdeaDeleteRequest).filter(IdeaDeleteRequest.status == "pending").count()

    return templates.TemplateResponse(
        request=request,
        name="admin/admin_ideas.html",
        context={
            "username": user.get("username", "Admin"),
            "ideas": idea_list,
            "pending_deletes": pending_deletes,
            **stats,
        },
    )


# ---------------- ADMIN IDEA DETAILS ----------------
@router.get("/admin_idea_details/{idea_id}", response_class=HTMLResponse)
def admin_idea_details(request: Request, idea_id: int, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    stats = get_admin_stats(db)
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        return RedirectResponse(url="/admin_ideas", status_code=303)

    import json as _json

    def safe_json_parse(value):
        if not value:
            return []
        try:
            return _json.loads(value)
        except (ValueError, TypeError):
            return []

    product_images = safe_json_parse(idea.product_images)
    founders = safe_json_parse(idea.founders)
    existing_investors = safe_json_parse(idea.existing_investors)
    ip_docs = safe_json_parse(idea.ip_document_paths)
    creator = db.query(User).filter(User.id == idea.user_id).first()

    # Admin notes for this idea
    admin_notes = (
        db.query(IdeaAdminNote)
        .filter(IdeaAdminNote.idea_id == idea_id)
        .order_by(IdeaAdminNote.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/admin_idea_details.html",
        context={
            "username": user.get("username", "Admin"),
            "idea": idea,
            "product_images": product_images,
            "founders": founders,
            "existing_investors": existing_investors,
            "ip_docs": ip_docs,
            "creator": creator,
            "admin_notes": admin_notes,
            **stats,
        },
    )


# ---------------- ADMIN IDEA STATUS UPDATE ----------------
@router.post("/admin_idea_status/{idea_id}")
async def admin_idea_status(request: Request, idea_id: int, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    form = await request.form()
    new_status = form.get("status", "").strip()
    admin_notes_text = form.get("admin_notes", "").strip()

    if new_status not in ("approved", "rejected", "changes_requested", "reviewing"):
        return RedirectResponse(url=f"/admin_idea_details/{idea_id}", status_code=303)

    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        return RedirectResponse(url="/admin_ideas", status_code=303)

    idea.status = new_status
    idea.updated_at = datetime.now(timezone.utc)

    if admin_notes_text:
        note_type = "rejection_reason" if new_status == "rejected" else (
            "changes_requested" if new_status == "changes_requested" else "approval_note"
        )
        note = IdeaAdminNote(
            idea_id=idea_id,
            note=admin_notes_text,
            note_type=note_type,
        )
        db.add(note)

    db.commit()
    return RedirectResponse(url=f"/admin_idea_details/{idea_id}", status_code=303)


# ---------------- ADMIN DELETE REQUESTS ----------------
@router.get("/admin_delete_requests", response_class=HTMLResponse)
def admin_delete_requests(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    stats = get_admin_stats(db)
    delete_requests = (
        db.query(IdeaDeleteRequest)
        .order_by(IdeaDeleteRequest.created_at.desc())
        .all()
    )

    requests_data = []
    for req in delete_requests:
        idea = db.query(Idea).filter(Idea.id == req.idea_id).first()
        creator = db.query(User).filter(User.id == req.creator_user_id).first()
        requests_data.append({
            "id": req.id,
            "idea_id": req.idea_id,
            "idea_title": idea.title if idea else "Deleted",
            "creator_name": creator.username if creator else "Unknown",
            "creator_email": creator.email if creator else "",
            "reason": req.reason,
            "status": req.status,
            "admin_notes": req.admin_notes,
            "created_at": req.created_at,
            "reviewed_at": req.reviewed_at,
        })

    return templates.TemplateResponse(
        request=request,
        name="admin/admin_delete_requests.html",
        context={
            "username": user.get("username", "Admin"),
            "delete_requests": requests_data,
            **stats,
        },
    )


@router.post("/admin_delete_requests/approve/{req_id}")
async def approve_delete_request(request: Request, req_id: int, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    form = await request.form()
    admin_notes = form.get("admin_notes", "").strip()

    req = db.query(IdeaDeleteRequest).filter(IdeaDeleteRequest.id == req_id).first()
    if req and req.status == "pending":
        req.status = "approved"
        req.admin_notes = admin_notes
        req.reviewed_at = datetime.now(timezone.utc)

        idea = db.query(Idea).filter(Idea.id == req.idea_id).first()
        if idea:
            idea.status = "deleted"
            idea.is_draft = "true"

        db.commit()

    return RedirectResponse(url="/admin_delete_requests", status_code=303)


@router.post("/admin_delete_requests/reject/{req_id}")
async def reject_delete_request(request: Request, req_id: int, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "admin":
        return RedirectResponse(url="/login", status_code=303)

    form = await request.form()
    admin_notes = form.get("admin_notes", "").strip()

    req = db.query(IdeaDeleteRequest).filter(IdeaDeleteRequest.id == req_id).first()
    if req and req.status == "pending":
        req.status = "rejected"
        req.admin_notes = admin_notes
        req.reviewed_at = datetime.now(timezone.utc)
        db.commit()

    return RedirectResponse(url="/admin_delete_requests", status_code=303)
