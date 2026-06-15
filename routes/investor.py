from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from services.investor_service import get_investor_dashboard_data

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/investor_dashboard", response_class=HTMLResponse)
async def investor_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    if not user or user.get("role") != "investor":
        return RedirectResponse(url="/login", status_code=303)

    context = get_investor_dashboard_data(db, user)
    return templates.TemplateResponse(
        request=request,
        name="investor/investor_dashboard.html",
        context=context,
    )
