from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# =========================
# ADMIN DASHBOARD
# =========================
@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):

    # Get session user
    user = request.session.get("user")

    # =========================
    # NOT LOGGED IN
    # =========================
    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # =========================
    # NOT ADMIN
    # =========================
    if user.get("role") != "admin":

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # =========================
    # ADMIN DASHBOARD DATA
    # =========================
    return templates.TemplateResponse(
        request=request,
        name="admin/admin_dashboard.html",
        context={
            "username": user.get("username", "Admin"),
            "total_users": 120,   # later from DB
            "total_ideas": 45     # later from DB
        }
    )
