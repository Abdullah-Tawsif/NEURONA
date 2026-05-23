from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")


# HOME PAGE
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home/index.html",
        context={}
    )


# signup + LOGIN PAGES (both /signup and /signup routes)
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/signup.html",
        context={}
    )


@app.get("/signup", response_class=HTMLResponse)
async def signup_alias(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/signup.html",
        context={}
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={}
    )


# SIGNUP FORM SUBMIT
@app.post("/signup", response_class=HTMLResponse)
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
            context={"message": "Passwords do not match."}
        )

    allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "neurona.com"]
    domain = email.split("@")[-1].lower()
    if domain not in allowed_domains:
        return templates.TemplateResponse(
            request=request,
            name="auth/signup.html",
            context={"message": "Email domain not allowed."}
        )

    return templates.TemplateResponse(
        request=request,
        name="auth/signup.html",
        context={"message": f"Account created successfully for {username}! You can now log in."}
    )


# LOGIN FORM SUBMIT
@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    if email == "admin@gmail.com" and password == "1234":
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={"message": "Invalid email or password"}
    )
