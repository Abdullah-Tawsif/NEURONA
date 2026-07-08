import json

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from models.creator_verification import CreatorVerification
from models.idea import Idea
from models.user import User
from services.creator_service import get_creator_dashboard_data, create_creator_verification
from services.idea_service import (
    get_upload_idea_context,
    create_idea,
    update_idea,
    get_idea_by_id,
    get_idea_by_submission_id,
    get_draft,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/creator_dashboard", response_class=HTMLResponse)
async def creator_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    if not user or user.get("role") != "creator":
        return RedirectResponse(url="/login", status_code=303)

    context = get_creator_dashboard_data(db, user)
    submitted = request.query_params.get("submitted") == "1"
    already_submitted = request.query_params.get("already_submitted") == "1"
    context["submitted"] = submitted
    context["already_submitted"] = already_submitted
    return templates.TemplateResponse(
        request=request,
        name="creator/creator_dashboard.html",
        context=context,
    )

# verify_creator
@router.get("/verify_creator", response_class=HTMLResponse)
async def verify_creator_page(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "creator":
        return RedirectResponse(url="/login", status_code=303)

    existing = (
        db.query(CreatorVerification)
        .filter(CreatorVerification.user_id == user["id"])
        .first()
    )
    if existing and existing.status == "pending":
        return RedirectResponse(
            url="/creator_dashboard?already_submitted=1",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="creator/verify_creator.html",
        context={
            "email": user.get("email"),
        },
    )


@router.post("/verify_creator")
async def verify_creator(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    gov_id: str = Form(...),
    linkedin_id: str = Form(...),
    present_address: str = Form(...),
    db: Session = Depends(get_db),
):

    user = request.session.get("user")

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    verification = create_creator_verification(
        db=db,
        user_id=user["id"],
        full_name=full_name,
        phone=phone,
        gov_id=gov_id,
        linkedin_id=linkedin_id,
        present_address=present_address,
    )

    if verification is None:
        return RedirectResponse(
            url="/creator_dashboard?already_submitted=1",
            status_code=303,
        )

    return RedirectResponse(
        url="/creator_dashboard?submitted=1",
        status_code=303,
    )

# Creator Profile
@router.get("/creator_profile", response_class=HTMLResponse)
async def creator_profile(request: Request, db: Session = Depends(get_db)):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    # Initialize stats based on the logged-in user's actual role
    if user.get("role") == "creator":
        stats = {
            "total_ideas": 0,
            "total_investments": 0,
            "total_funding": 0
        }

    return templates.TemplateResponse(
        request=request,
        name="creator/creator_profile.html",
        context={
            "user": user,
            "stats": stats
        }
    )


# Dismiss verified popup
@router.post("/dismiss_verified_popup")
async def dismiss_verified_popup(
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    if not user:
        return JSONResponse({"success": False}, status_code=401)

    db_user = db.query(User).filter(User.id == user.get("id")).first()
    if db_user:
        db_user.verified_popup_shown = True
        db.commit()

    return JSONResponse({"success": True})


# ==================== UPLOAD IDEA ====================

@router.get("/upload_idea", response_class=HTMLResponse)
async def upload_idea_page(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "creator":
        return RedirectResponse(url="/login", status_code=303)

    creator = db.query(User).filter(User.id == user["id"]).first()
    if not creator or not creator.is_verified:
        return RedirectResponse(
            url="/creator_dashboard?verify_required=1",
            status_code=303,
        )

    context = get_upload_idea_context(db, user)

    draft = get_draft(db, user["id"])
    if draft:
        context["draft"] = draft
        context["draft_id"] = draft.id

    return templates.TemplateResponse(
        request=request,
        name="creator/upload_idea.html",
        context=context,
    )


@router.post("/upload_idea")
async def upload_idea_submit(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(""),
    category: str = Form(""),
    other_category: str = Form(""),
    current_status: str = Form(""),
    tags: str = Form(""),
    target_market: str = Form(""),
    summary: str = Form(""),
    problem_statement: str = Form(""),
    proposed_solution: str = Form(""),
    full_name: str = Form(""),
    email: str = Form(""),
    contact_number: str = Form(""),
    founders: str = Form("[]"),
    company_website: str = Form(""),
    team_size: str = Form("0"),
    address: str = Form(""),
    country: str = Form(""),
    funding_goal: str = Form("0"),
    currency: str = Form("BDT"),
    product_stage: str = Form(""),
    equity_offered: str = Form("0"),
    funding_usage: str = Form(""),
    expected_timeline: str = Form(""),
    revenue_status: str = Form(""),
    monthly_revenue: str = Form(""),
    existing_investors: str = Form("[]"),
    intellectual_property: str = Form(""),
    product_demo_url: str = Form(""),
    business_plan: UploadFile = File(None),
    product_images: list[UploadFile] = File([]),
    ip_documents: list[UploadFile] = File([]),
    demo_video: UploadFile = File(None),
    is_draft: str = Form("false"),
    draft_id: str = Form(""),
):
    user = request.session.get("user")
    if not user or user.get("role") != "creator":
        return RedirectResponse(url="/login", status_code=303)

    creator = db.query(User).filter(User.id == user["id"]).first()
    if not creator or not creator.is_verified:
        return RedirectResponse(
            url="/creator_dashboard?verify_required=1",
            status_code=303,
        )

    form_data = {
        "title": title,
        "category": category,
        "other_category": other_category,
        "current_status": current_status,
        "tags": tags,
        "target_market": target_market,
        "summary": summary,
        "problem_statement": problem_statement,
        "proposed_solution": proposed_solution,
        "full_name": full_name,
        "email": email,
        "contact_number": contact_number,
        "founders": founders,
        "company_website": company_website,
        "team_size": team_size,
        "address": address,
        "country": country,
        "funding_goal": funding_goal,
        "currency": currency,
        "product_stage": product_stage,
        "equity_offered": equity_offered,
        "funding_usage": funding_usage,
        "expected_timeline": expected_timeline,
        "revenue_status": revenue_status,
        "monthly_revenue": monthly_revenue,
        "existing_investors": existing_investors,
        "intellectual_property": intellectual_property,
        "product_demo_url": product_demo_url,
    }

    draft_mode = is_draft == "true"

    existing_idea = None
    if draft_id:
        existing_idea = get_idea_by_id(db, int(draft_id), user["id"])

    if not existing_idea and draft_mode:
        existing_idea = get_draft(db, user["id"])

    if existing_idea:
        idea, error = update_idea(
            db, existing_idea, form_data,
            business_plan, product_images, ip_documents, demo_video,
            is_draft=draft_mode,
        )
    else:
        idea, error = create_idea(
            db, user["id"], form_data,
            business_plan, product_images, ip_documents, demo_video,
            is_draft=draft_mode,
        )

    if draft_mode:
        if idea:
            return JSONResponse({"success": True, "draft_id": idea.id})
        return JSONResponse({"success": False, "error": error or "Failed to save draft"}, status_code=400)

    if error:
        context = get_upload_idea_context(db, user)
        context["error"] = error
        context["form_data"] = form_data
        return templates.TemplateResponse(
            request=request,
            name="creator/upload_idea.html",
            context=context,
        )

    return RedirectResponse(
        url=f"/upload_idea/success/{idea.submission_id}",
        status_code=303,
    )


@router.get("/upload_idea/success/{submission_id}", response_class=HTMLResponse)
async def upload_idea_success(
    request: Request,
    submission_id: str,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    if not user or user.get("role") != "creator":
        return RedirectResponse(url="/login", status_code=303)

    idea = get_idea_by_submission_id(db, submission_id)
    if not idea or idea.user_id != user["id"]:
        return RedirectResponse(url="/creator_dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="creator/upload_idea_success.html",
        context={
            "submission_id": idea.submission_id,
            "idea_id": idea.id,
            "idea_title": idea.title,
        },
    )


@router.get("/creator_idea_details/{idea_id}", response_class=HTMLResponse)
async def creator_idea_details(
    request: Request,
    idea_id: int,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    if not user or user.get("role") != "creator":
        return RedirectResponse(url="/login", status_code=303)

    idea = get_idea_by_id(db, idea_id, user["id"])
    if not idea:
        return RedirectResponse(url="/creator_dashboard", status_code=303)

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

    return templates.TemplateResponse(
        request=request,
        name="creator/creator_idea_details.html",
        context={
            "idea": idea,
            "product_images": product_images,
            "founders": founders,
            "existing_investors": existing_investors,
            "ip_docs": ip_docs,
        },
    )
