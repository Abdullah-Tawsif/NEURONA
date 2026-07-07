from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import get_db
from services.auth_service import authenticate_user, register_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

LOGIN_REDIRECT = "/login"
SIGNUP_TEMPLATE = "auth/signup.html"
LOGIN_TEMPLATE = "auth/login.html"


def _redirect_by_role(role: str) -> RedirectResponse:
    targets = {
        "admin": "/admin",
        "creator": "/creator_dashboard",
        "investor": "/investor_dashboard",
    }
    return RedirectResponse(url=targets.get(role, "/"), status_code=303)


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name=SIGNUP_TEMPLATE, context={})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name=LOGIN_TEMPLATE, context={})


@router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db),
):
    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name=SIGNUP_TEMPLATE,
            context={"message": "Passwords do not match", "message_type": "error"},
        )

    user, error = register_user(db, username, email, password, role)
    if error:
        return templates.TemplateResponse(
            request=request,
            name=SIGNUP_TEMPLATE,
            context={"message": error, "message_type": "error"},
        )

    return templates.TemplateResponse(
        request=request,
        name=SIGNUP_TEMPLATE,
        context={"message": f"Account created successfully for {username}", "message_type": "success"},
    )


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    session_data = authenticate_user(db, email, password)
    if not session_data:
        return templates.TemplateResponse(
            request=request,
            name=LOGIN_TEMPLATE,
            context={"message": "Invalid email or password", "message_type": "error"},
        )

    request.session["user"] = session_data
    return _redirect_by_role(session_data["role"])


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=LOGIN_REDIRECT, status_code=303)
