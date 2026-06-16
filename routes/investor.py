from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from services.investor_service import get_investor_dashboard_data, create_investor_verification
from services.investor_service import has_existing_verification
from models.investor_verification import InvestorVerification

router = APIRouter()
templates = Jinja2Templates(directory="templates")

#investor_dashboard

@router.get("/investor_dashboard", response_class=HTMLResponse)
async def investor_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
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

# verify_investor
@router.get("/verify_investor", response_class=HTMLResponse)
async def verify_invesor_page(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user.get("role") != "investor":
        return RedirectResponse(url="/login", status_code=303)
    

    existing = (
        db.query(InvestorVerification)
        .filter(InvestorVerification.user_id == user["id"])
        .first()
    )
    if existing:
        return RedirectResponse(
            url="/investor_dashboard?already_submitted=1",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="investor/verify_investor.html",
        context={
            "email": user.get("email"),
        },
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
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

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
        return RedirectResponse(
            url="/investor_dashboard?already_submitted=1",
            status_code=303,
        )

    return RedirectResponse(
        url="/investor_dashboard?submitted=1",
        status_code=303,
    )

#Investor Profile

@router.get("/investor_profile", response_class=HTMLResponse)
async def investor_profile(request: Request, db: Session = Depends(get_db)):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    stats = {
        "active_investments": 0,
        "success_rate": 0,
        "total_invested": 0
    }

    #  FIXED: Using explicit keyword arguments
    return templates.TemplateResponse(
        request=request,
        name="investor/investor_profile.html",
        context={
            "user": user,
            "stats": stats
        }
    )
