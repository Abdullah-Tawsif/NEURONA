import json

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User
from models.idea import Idea
from services.investor_service import get_investor_dashboard_data, create_investor_verification
from services.investment_service import (
    toggle_bookmark,
    get_idea_investment_stats,
)
from models.investor_verification import InvestorVerification

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/investor_dashboard", response_class=HTMLResponse)
async def investor_dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "investor":
        return RedirectResponse(url="/login", status_code=303)

    context = get_investor_dashboard_data(db, user)
    submitted = request.query_params.get("submitted") == "1"
    already_submitted = request.query_params.get("already_submitted") == "1"
    context["submitted"] = submitted
    context["already_submitted"] = already_submitted
    return templates.TemplateResponse(
        request=request,
        name="investor/investor_dashboard.html",
        context=context,
    )


@router.get("/verify_investor", response_class=HTMLResponse)
async def verify_investor_page(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "investor":
        return RedirectResponse(url="/login", status_code=303)

    existing = (
        db.query(InvestorVerification)
        .filter(InvestorVerification.user_id == user["id"])
        .first()
    )
    if existing and existing.status == "pending":
        return RedirectResponse(url="/investor_dashboard?already_submitted=1", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="investor/verify_investor.html",
        context={"email": user.get("email")},
    )


@router.post("/verify_investor")
async def verify_investor(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    gov_id: str = Form(...),
    linkedin_id: str = Form(...),
    present_address: str = Form(...),
    mandatory_doc: UploadFile = File(...),
    optional_doc: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    verification = create_investor_verification(
        db=db,
        user_id=user["id"],
        full_name=full_name,
        phone=phone,
        gov_id=gov_id,
        linkedin_id=linkedin_id,
        present_address=present_address,
        mandatory_doc=mandatory_doc,
        optional_doc=optional_doc,
    )

    if verification is None:
        return RedirectResponse(url="/investor_dashboard?already_submitted=1", status_code=303)

    return RedirectResponse(url="/investor_dashboard?submitted=1", status_code=303)


@router.get("/investor_profile", response_class=HTMLResponse)
async def investor_profile(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    stats = {"active_investments": 0, "success_rate": 0, "total_invested": 0}
    return templates.TemplateResponse(
        request=request,
        name="investor/investor_profile.html",
        context={"user": user, "stats": stats},
    )


@router.get("/investor_idea_details/{idea_id}", response_class=HTMLResponse)
async def investor_idea_details(request: Request, idea_id: int, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "investor":
        return RedirectResponse(url="/login", status_code=303)

    # Only verified investors can see details
    db_user = db.query(User).filter(User.id == user["id"]).first()
    if not db_user or not db_user.is_verified:
        return RedirectResponse(url="/investor_dashboard", status_code=303)

    idea = db.query(Idea).filter(Idea.id == idea_id, Idea.status == "approved", Idea.is_draft == "false").first()
    if not idea:
        return RedirectResponse(url="/investor_dashboard", status_code=303)

    stats_raw = get_idea_investment_stats(db, idea_id)
    funding_goal = idea.funding_goal or 0
    progress = (stats_raw["total_raised"] / funding_goal * 100) if funding_goal > 0 else 0

    stats = {
        "total_raised": stats_raw["total_raised"],
        "investor_count": stats_raw["investor_count"],
        "equity_sold": stats_raw["equity_sold"],
        "progress": round(min(progress, 100), 1),
    }

    def safe_json_parse(value):
        if not value:
            return []
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return []

    product_images = safe_json_parse(idea.product_images)
    founders = safe_json_parse(idea.founders)
    existing_investors = safe_json_parse(idea.existing_investors)
    ip_docs = safe_json_parse(idea.ip_document_paths)

    return templates.TemplateResponse(
        request=request,
        name="investor/investor_idea_details.html",
        context={
            "idea": idea,
            "stats": stats,
            "product_images": product_images,
            "founders": founders,
            "existing_investors": existing_investors,
            "ip_docs": ip_docs,
            "user": user,
        },
    )


@router.post("/investor/bookmark/{idea_id}")
async def bookmark_idea(request: Request, idea_id: int, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "investor":
        return JSONResponse({"success": False}, status_code=401)

    bookmarked = toggle_bookmark(db, idea_id, user["id"])
    return JSONResponse({"success": True, "bookmarked": bookmarked})


@router.post("/dismiss_verified_popup")
async def dismiss_verified_popup(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        return JSONResponse({"success": False}, status_code=401)

    db_user = db.query(User).filter(User.id == user.get("id")).first()
    if db_user:
        db_user.verified_popup_shown = True
        db.commit()

    return JSONResponse({"success": True})
