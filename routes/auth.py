from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database.database import SessionLocal
from models.user import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# =========================
# SIGNUP PAGE
# =========================
@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/signup.html",
        context={}
    )


# =========================
# LOGIN PAGE
# =========================
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={}
    )


# =========================
# SIGNUP FORM
# =========================
@router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    role: str = Form(...)
):

    # Password check
    if password != confirm_password:

        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={
                "message": "Passwords do not match"
            }
        )

    # Allowed email domains
    allowed_domains = [
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "hotmail.com",
        "neurona.com"
    ]

    domain = email.split("@")[-1].lower()

    if domain not in allowed_domains:

        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={
                "message": "Email domain not allowed"
            }
        )

    # Database session
    db = SessionLocal()

    # Check existing email
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:

        db.close()

        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={
                "message": "Email already registered"
            }
        )

    # Create new user
    new_user = User(
        username=username,
        email=email,
        password=password,
        role=role
    )

    db.add(new_user)
    db.commit()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="auth/signup.html",
        context={
            "message":
            f"Account created successfully for {username}"
        }
    )


# =========================
# LOGIN FORM
# =========================
@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    # =========================
    # ADMIN LOGIN
    # =========================
    if email == "admin@neurona.com" and password == "1234":

        request.session["user"] = {
            "email": email,
            "role": "admin"
        }

        return RedirectResponse(
            url="/admin",
            status_code=303
        )

    # =========================
    # DATABASE LOGIN
    # =========================
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email,
        User.password == password
    ).first()

    db.close()

    # Invalid login
    if not user:

        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={
                "message": "Invalid email or password"
            }
        )

    # SAVE SESSION
    request.session["user"] = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

    # Creator
    if user.role == "creator":

        return RedirectResponse(
            url="/creator_dashboard",
            status_code=303
        )

    # Investor
    elif user.role == "investor":

        return RedirectResponse(
            url="/investor_dashboard",
            status_code=303
        )

    return RedirectResponse(
        url="/",
        status_code=303
    )

# =========================
# LOGOUT
# =========================
@router.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )
