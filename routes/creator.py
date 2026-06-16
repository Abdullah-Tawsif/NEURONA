from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from services.creator_service import get_creator_dashboard_data, create_creator_verification

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
async def verify_invesor_page(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "creator":
        return RedirectResponse(url="/login", status_code=303)

    from services.creator_service import has_existing_verification
    from models.creator_verification import CreatorVerification

    existing = (
        db.query(CreatorVerification)
        .filter(CreatorVerification.user_id == user["id"])
        .first()
    )
    if existing:
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
@router.get("/creator_profile", response_class=HTMLResponse)  # 
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
