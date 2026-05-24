from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# SIGNUP PAGE
@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/signup.html",
        context={}
    )


# LOGIN PAGE
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={}
    )


# SIGNUP FORM
@router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    role: str = Form(...)
):

    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={"message": "Passwords do not match"}
        )

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
            context={"message": "Email domain not allowed"}
        )

    return templates.TemplateResponse(
        request=request,
        name="auth/signup.html",
        context={
            "message":
            f"Account created successfully for {username}"
        }
    )


# LOGIN FORM
@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    if email == "admin@neurona.com" and password == "1234":
        return RedirectResponse(url="/admin", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={"message": "Invalid email or password"}
    )