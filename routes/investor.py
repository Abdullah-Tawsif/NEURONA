from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/investor_dashboard", response_class=HTMLResponse)
async def investor_dashboard(request: Request):

    user = request.session.get("user")

    # NOT LOGGED IN
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    # ROLE CHECK
    if user.get("role") != "investor":
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="investor/investor_dashboard.html",
        context={
            "username": user.get("username"),
            "verified": 0,   # default simple value
            "ideas": []      # empty for now
        }
    )