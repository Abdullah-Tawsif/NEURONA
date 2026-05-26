from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# =========================
# CREATOR DASHBOARD
# =========================
@router.get("/creator_dashboard", response_class=HTMLResponse)
async def creator_dashboard(request: Request):

    # =========================
    # SESSION USER
    # =========================
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
    # NOT CREATOR
    # =========================
    if user.get("role") != "creator":

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # =========================
    # DUMMY DATA (LATER DB)
    # =========================
    creator_name = user.get("username", "Creator")
    verified = 1   # later from DB

    creator_ideas = []  # later from Ideas table

    # =========================
    # RENDER DASHBOARD
    # =========================
    return templates.TemplateResponse(
        request=request,
        name="creator/creator_dashboard.html",
        context={
            "creator_name": creator_name,
            "verified": verified,
            "creator_ideas": creator_ideas
        }
    )