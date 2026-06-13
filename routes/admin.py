from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ADMIN DASHBOARD
@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):

    # Get session user
    user = request.session.get("user")

    # NOT LOGGED IN
    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # NOT ADMIN
    if user.get("role") != "admin":

        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    total_users = db.query(User).count()

    # ADMIN DASHBOARD DATA
    return templates.TemplateResponse(
        request=request,
        name="admin/admin_dashboard.html",
        context={
            "username": user.get("username", "Admin"),
            "total_users": total_users,
            "total_ideas": 45     # later from DB
        }
    )
