import json
import os
import re
import uuid
import shutil
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.idea import Idea
from models.user import User

BUSINESS_PLAN_FOLDER = "static/uploads/business_plans"
PRODUCT_IMAGES_FOLDER = "static/uploads/product_images"
IP_DOCUMENTS_FOLDER = "static/uploads/intellectual_property"
DEMOS_FOLDER = "static/uploads/demos"

for folder in [
    BUSINESS_PLAN_FOLDER,
    PRODUCT_IMAGES_FOLDER,
    IP_DOCUMENTS_FOLDER,
    DEMOS_FOLDER,
]:
    os.makedirs(folder, exist_ok=True)

ALLOWED_BUSINESS_PLAN_EXT = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".jpg", ".jpeg", ".png"}
ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_IP_EXT = {".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"}
ALLOWED_VIDEO_EXT = {".mp4", ".mov", ".avi", ".webm", ".mkv"}

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_VIDEO_SIZE = 50 * 1024 * 1024

COUNTRIES = [
    "Bangladesh", "India", "Pakistan", "United States", "United Kingdom",
    "Canada", "Australia", "Germany", "France", "Singapore",
    "Japan", "China", "Brazil", "Mexico", "Netherlands",
    "Sweden", "Switzerland", "United Arab Emirates", "Saudi Arabia", "Other",
]

CURRENCIES = ["BDT", "USD", "EUR", "GBP", "INR"]

CATEGORIES = [
    "Technology", "Artificial Intelligence (AI)", "Healthcare", "Education",
    "Finance", "Environment", "Agriculture", "E-commerce", "Robotics",
    "Cybersecurity", "Biotechnology", "Energy", "Transportation",
    "Real Estate", "Social Impact", "Entertainment", "Other",
]

CURRENT_STATUSES = [
    "Looking for Investment", "Looking for Co-founder",
    "Looking for Mentor", "Looking for Strategic Partner",
]

TARGET_MARKETS = ["Students", "Businesses", "Hospitals", "Government", "Consumers"]

PRODUCT_STAGES = ["Idea", "Prototype", "MVP", "Beta", "Launched", "Growth"]

TIMELINES = ["Immediately", "Within 3 Months", "Within 6 Months", "Within 1 Year"]

REVENUE_STATUSES = ["Pre-revenue", "Generating Revenue", "Profitable"]

PHONE_COUNTRIES = [
    {"code": "+880", "name": "Bangladesh", "flag": "🇧🇩"},
    {"code": "+91", "name": "India", "flag": "🇮🇳"},
    {"code": "+92", "name": "Pakistan", "flag": "🇵🇰"},
    {"code": "+1", "name": "USA", "flag": "🇺🇸"},
    {"code": "+44", "name": "UK", "flag": "🇬🇧"},
    {"code": "+1", "name": "Canada", "flag": "🇨🇦"},
    {"code": "+61", "name": "Australia", "flag": "🇦🇺"},
]


def generate_submission_id(db: Session) -> str:
    year = datetime.now(timezone.utc).year
    prefix = f"NRN-{year}-"
    count = db.query(Idea).filter(Idea.submission_id.like(f"{prefix}%")).count()
    sequential = count + 1
    return f"{prefix}{sequential:06d}"


def save_file(upload_file, folder, allowed_ext, max_size):
    if upload_file is None or not upload_file.filename:
        return None, "No file provided"

    ext = os.path.splitext(upload_file.filename)[1].lower()
    if ext not in allowed_ext:
        return None, f"File type {ext} not allowed"

    upload_file.file.seek(0, 2)
    size = upload_file.file.tell()
    upload_file.file.seek(0)

    if size > max_size:
        return None, f"File size exceeds {max_size // (1024 * 1024)}MB limit"

    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return filepath, None


def save_multiple_files(files, folder, allowed_ext, max_size):
    paths = []
    errors = []
    for f in files:
        if f is None or not f.filename:
            continue
        path, err = save_file(f, folder, allowed_ext, max_size)
        if err:
            errors.append(err)
        else:
            paths.append(path)
    return paths, errors


def validate_email(email: str) -> bool:
    if not email:
        return False
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


def validate_linkedin(url: str) -> bool:
    if not url:
        return False
    return bool(re.match(
        r"^(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%]+/?$", url
    ))


def validate_website(url: str) -> bool:
    if not url:
        return True
    return bool(re.match(
        r"^(https?://)?(www\.)?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(/.*)?$", url
    ))


def validate_phone(phone: str) -> bool:
    if not phone:
        return False
    return bool(re.match(r"^\+?\d{6,15}$", phone.replace(" ", "").replace("-", "")))


def validate_title(title: str) -> bool:
    if not title:
        return False
    return len(title.strip().split()) <= 8


def validate_other_category(other: str) -> bool:
    if not other:
        return True
    return len(other.strip().split()) <= 2


def get_creator_ideas(db: Session, user_id: int) -> list:
    return db.query(Idea).filter(Idea.user_id == user_id).order_by(Idea.created_at.desc()).all()


def get_idea_by_id(db: Session, idea_id: int, user_id: int = None) -> Idea | None:
    query = db.query(Idea).filter(Idea.id == idea_id)
    if user_id is not None:
        query = query.filter(Idea.user_id == user_id)
    return query.first()


def get_all_ideas(db: Session) -> list:
    return db.query(Idea).order_by(Idea.created_at.desc()).all()


def get_idea_by_submission_id(db: Session, submission_id: str) -> Idea | None:
    return db.query(Idea).filter(Idea.submission_id == submission_id).first()


def get_upload_idea_context(db: Session, user: dict) -> dict:
    creator = db.query(User).filter(User.id == user.get("id")).first()
    verification = db.query(User).filter(User.id == user.get("id")).first()

    full_name = user.get("username", "")
    if verification:
        from models.creator_verification import CreatorVerification
        cv = db.query(CreatorVerification).filter(
            CreatorVerification.user_id == user.get("id")
        ).first()
        if cv:
            full_name = cv.full_name

    return {
        "email": user.get("email", ""),
        "full_name": full_name,
        "countries": COUNTRIES,
        "currencies": CURRENCIES,
        "categories": CATEGORIES,
        "current_statuses": CURRENT_STATUSES,
        "target_markets": TARGET_MARKETS,
        "product_stages": PRODUCT_STAGES,
        "timelines": TIMELINES,
        "revenue_statuses": REVENUE_STATUSES,
        "phone_countries": PHONE_COUNTRIES,
        "is_verified": creator.is_verified if creator else False,
    }


def create_idea(
    db: Session,
    user_id: int,
    form_data: dict,
    business_plan,
    product_images,
    ip_documents,
    demo_video,
    is_draft: bool = False,
) -> tuple[Idea | None, str | None]:
    errors = []

    title = form_data.get("title", "").strip()
    if not is_draft and not validate_title(title):
        errors.append("Title must be 8 words or less")

    category = form_data.get("category", "")
    other_category = form_data.get("other_category", "").strip()
    if not is_draft:
        if not category:
            errors.append("Category is required")
        if "Other" in (category.split(",") if category else []) and not validate_other_category(other_category):
            errors.append("Other category must be 2 words or less")

    current_status = form_data.get("current_status", "")
    target_market = form_data.get("target_market", "")
    summary = form_data.get("summary", "").strip()
    problem_statement = form_data.get("problem_statement", "").strip()
    proposed_solution = form_data.get("proposed_solution", "").strip()

    if not is_draft:
        if not current_status:
            errors.append("Current status is required")
        if not target_market:
            errors.append("Target market is required")
        if not summary:
            errors.append("Summary is required")
        if not problem_statement:
            errors.append("Problem statement is required")
        if not proposed_solution:
            errors.append("Proposed solution is required")

    full_name = form_data.get("full_name", "").strip()
    email = form_data.get("email", "").strip()
    contact_number = form_data.get("contact_number", "").strip()
    founders = form_data.get("founders", "[]")
    company_website = form_data.get("company_website", "").strip()
    team_size = form_data.get("team_size", "0")
    address = form_data.get("address", "").strip()
    country = form_data.get("country", "")

    if not is_draft:
        if not full_name:
            errors.append("Full name is required")
        if not validate_email(email):
            errors.append("Valid email is required")
        if not validate_phone(contact_number):
            errors.append("Valid contact number is required")
        if not founders or founders == "[]":
            errors.append("At least one founder is required")
        if company_website and not validate_website(company_website):
            errors.append("Invalid website URL")
        try:
            ts = int(team_size)
            if ts < 1:
                errors.append("Team size must be at least 1")
        except (ValueError, TypeError):
            if not is_draft:
                errors.append("Team size must be a number")
            ts = 0
        if not address:
            errors.append("Address is required")
        if not country:
            errors.append("Country is required")
    else:
        try:
            ts = int(team_size) if team_size else 0
        except (ValueError, TypeError):
            ts = 0

    funding_goal = form_data.get("funding_goal", "0")
    currency = form_data.get("currency", "BDT")
    product_stage = form_data.get("product_stage", "")
    equity_offered = form_data.get("equity_offered", "0")
    funding_usage = form_data.get("funding_usage", "").strip()
    expected_timeline = form_data.get("expected_timeline", "")
    revenue_status = form_data.get("revenue_status", "")
    monthly_revenue = form_data.get("monthly_revenue", "")
    existing_investors = form_data.get("existing_investors", "[]")
    intellectual_property = form_data.get("intellectual_property", "")

    if not is_draft:
        try:
            fg = float(funding_goal)
            if fg < 50:
                errors.append("Funding goal must be at least 50")
        except (ValueError, TypeError):
            errors.append("Funding goal must be a number")
            fg = 0
        if not product_stage:
            errors.append("Product stage is required")
        try:
            eq = float(equity_offered)
            if eq < 0 or eq > 100:
                errors.append("Equity must be between 0 and 100")
        except (ValueError, TypeError):
            errors.append("Equity must be a number")
            eq = 0
        if not currency:
            errors.append("Currency is required")
        if not funding_usage:
            errors.append("Funding usage is required")
        if not expected_timeline:
            errors.append("Expected timeline is required")
        if not revenue_status:
            errors.append("Revenue status is required")
    else:
        try:
            fg = float(funding_goal) if funding_goal else 0
        except (ValueError, TypeError):
            fg = 0
        try:
            eq = float(equity_offered) if equity_offered else 0
        except (ValueError, TypeError):
            eq = 0

    try:
        mr = float(monthly_revenue) if monthly_revenue else None
    except (ValueError, TypeError):
        mr = None

    business_plan_path = None
    if business_plan and business_plan.filename:
        business_plan_path, err = save_file(
            business_plan, BUSINESS_PLAN_FOLDER, ALLOWED_BUSINESS_PLAN_EXT, MAX_FILE_SIZE
        )
        if err and not is_draft:
            errors.append(f"Business plan: {err}")

    product_image_paths = []
    if product_images:
        valid_images = [f for f in product_images if f and f.filename]
        if not is_draft and len(valid_images) == 0:
            errors.append("At least one product image is required")
        product_image_paths, img_errors = save_multiple_files(
            valid_images, PRODUCT_IMAGES_FOLDER, ALLOWED_IMAGE_EXT, MAX_IMAGE_SIZE
        )
        for e in img_errors:
            if not is_draft:
                errors.append(f"Product image: {e}")

    ip_doc_paths = []
    if ip_documents:
        valid_docs = [f for f in ip_documents if f and f.filename]
        ip_doc_paths, ip_errors = save_multiple_files(
            valid_docs, IP_DOCUMENTS_FOLDER, ALLOWED_IP_EXT, MAX_FILE_SIZE
        )
        for e in ip_errors:
            if not is_draft:
                errors.append(f"IP document: {e}")

    demo_video_path = None
    if demo_video and demo_video.filename:
        demo_video_path, err = save_file(
            demo_video, DEMOS_FOLDER, ALLOWED_VIDEO_EXT, MAX_VIDEO_SIZE
        )
        if err and not is_draft:
            errors.append(f"Demo video: {err}")

    product_demo_url = form_data.get("product_demo_url", "").strip()

    if not is_draft and errors:
        return None, "; ".join(errors)

    submission_id = generate_submission_id(db)

    idea = Idea(
        submission_id=submission_id,
        user_id=user_id,
        title=title,
        category=category,
        other_category=other_category if "Other" in (category.split(",") if category else []) else None,
        current_status=current_status,
        tags=form_data.get("tags", ""),
        target_market=target_market,
        summary=summary,
        problem_statement=problem_statement,
        proposed_solution=proposed_solution,
        full_name=full_name,
        email=email,
        contact_number=contact_number,
        founders=founders,
        company_website=company_website or None,
        team_size=ts,
        address=address,
        country=country,
        funding_goal=fg,
        currency=currency,
        product_stage=product_stage,
        equity_offered=eq,
        funding_usage=funding_usage,
        expected_timeline=expected_timeline,
        revenue_status=revenue_status,
        monthly_revenue=mr,
        existing_investors=existing_investors,
        business_plan_path=business_plan_path or "",
        product_images=json.dumps(product_image_paths),
        intellectual_property=intellectual_property,
        ip_document_paths=json.dumps(ip_doc_paths) if ip_doc_paths else None,
        product_demo_url=product_demo_url or None,
        product_demo_video_path=demo_video_path,
        status="draft" if is_draft else "submitted",
        is_draft="true" if is_draft else "false",
    )

    db.add(idea)
    db.commit()
    db.refresh(idea)

    return idea, None


def update_idea(
    db: Session,
    idea: Idea,
    form_data: dict,
    business_plan,
    product_images,
    ip_documents,
    demo_video,
    is_draft: bool = False,
) -> tuple[Idea | None, str | None]:
    errors = []

    title = form_data.get("title", "").strip()
    category = form_data.get("category", "")
    other_category = form_data.get("other_category", "").strip()
    current_status = form_data.get("current_status", "")
    target_market = form_data.get("target_market", "")
    summary = form_data.get("summary", "").strip()
    problem_statement = form_data.get("problem_statement", "").strip()
    proposed_solution = form_data.get("proposed_solution", "").strip()

    full_name = form_data.get("full_name", "").strip()
    email = form_data.get("email", "").strip()
    contact_number = form_data.get("contact_number", "").strip()
    founders_raw = form_data.get("founders", "[]")
    company_website = form_data.get("company_website", "").strip()
    team_size_raw = form_data.get("team_size", "0")
    address = form_data.get("address", "").strip()
    country = form_data.get("country", "")

    funding_goal_raw = form_data.get("funding_goal", "0")
    currency = form_data.get("currency", "BDT")
    product_stage = form_data.get("product_stage", "")
    equity_raw = form_data.get("equity_offered", "0")
    funding_usage = form_data.get("funding_usage", "").strip()
    expected_timeline = form_data.get("expected_timeline", "")
    revenue_status = form_data.get("revenue_status", "")
    monthly_revenue_raw = form_data.get("monthly_revenue", "")
    existing_investors_raw = form_data.get("existing_investors", "[]")
    intellectual_property = form_data.get("intellectual_property", "")
    product_demo_url = form_data.get("product_demo_url", "").strip()

    if not is_draft:
        if not validate_title(title):
            errors.append("Title must be 8 words or less")
        if not category:
            errors.append("Category is required")
        if not current_status:
            errors.append("Current status is required")
        if not target_market:
            errors.append("Target market is required")
        if not summary:
            errors.append("Summary is required")
        if not problem_statement:
            errors.append("Problem statement is required")
        if not proposed_solution:
            errors.append("Proposed solution is required")
        if not full_name:
            errors.append("Full name is required")
        if not validate_email(email):
            errors.append("Valid email is required")
        if not validate_phone(contact_number):
            errors.append("Valid contact number is required")
        if company_website and not validate_website(company_website):
            errors.append("Invalid website URL")
        if not address:
            errors.append("Address is required")
        if not country:
            errors.append("Country is required")
        if not product_stage:
            errors.append("Product stage is required")
        if not funding_usage:
            errors.append("Funding usage is required")
        if not expected_timeline:
            errors.append("Expected timeline is required")
        if not revenue_status:
            errors.append("Revenue status is required")
        if not currency:
            errors.append("Currency is required")

    try:
        founders = json.loads(founders_raw) if founders_raw else []
    except (json.JSONDecodeError, TypeError):
        founders = []
        founders_raw = "[]"
    if not is_draft and len(founders) == 0:
        errors.append("At least one founder is required")

    try:
        existing_investors = json.loads(existing_investors_raw) if existing_investors_raw else []
    except (json.JSONDecodeError, TypeError):
        existing_investors = []
        existing_investors_raw = "[]"

    try:
        team_size = int(team_size_raw) if team_size_raw else 0
    except (ValueError, TypeError):
        team_size = 0
        if not is_draft:
            errors.append("Team size must be a number")

    try:
        funding_goal = float(funding_goal_raw) if funding_goal_raw else 0
    except (ValueError, TypeError):
        funding_goal = 0
        if not is_draft:
            errors.append("Funding goal must be a number")
    if not is_draft and funding_goal < 50:
        errors.append("Funding goal must be at least 50")

    try:
        equity = float(equity_raw) if equity_raw else 0
    except (ValueError, TypeError):
        equity = 0
        if not is_draft:
            errors.append("Equity must be a number")
    if not is_draft and (equity < 0 or equity > 100):
        errors.append("Equity must be between 0 and 100")

    try:
        monthly_revenue = float(monthly_revenue_raw) if monthly_revenue_raw else None
    except (ValueError, TypeError):
        monthly_revenue = None

    if business_plan and business_plan.filename:
        path, err = save_file(business_plan, BUSINESS_PLAN_FOLDER, ALLOWED_BUSINESS_PLAN_EXT, MAX_FILE_SIZE)
        if err:
            errors.append(f"Business plan: {err}")
        else:
            idea.business_plan_path = path

    if product_images:
        valid_images = [f for f in product_images if f and f.filename]
        new_paths, img_errors = save_multiple_files(
            valid_images, PRODUCT_IMAGES_FOLDER, ALLOWED_IMAGE_EXT, MAX_IMAGE_SIZE
        )
        try:
            existing = json.loads(idea.product_images) if idea.product_images else []
        except (json.JSONDecodeError, TypeError):
            existing = []
        idea.product_images = json.dumps(existing + new_paths)
        for e in img_errors:
            errors.append(f"Product image: {e}")

    if ip_documents:
        valid_docs = [f for f in ip_documents if f and f.filename]
        new_ip_paths, ip_errors = save_multiple_files(
            valid_docs, IP_DOCUMENTS_FOLDER, ALLOWED_IP_EXT, MAX_FILE_SIZE
        )
        try:
            existing_ip = json.loads(idea.ip_document_paths) if idea.ip_document_paths else []
        except (json.JSONDecodeError, TypeError):
            existing_ip = []
        idea.ip_document_paths = json.dumps(existing_ip + new_ip_paths)
        for e in ip_errors:
            errors.append(f"IP document: {e}")

    if demo_video and demo_video.filename:
        path, err = save_file(demo_video, DEMOS_FOLDER, ALLOWED_VIDEO_EXT, MAX_VIDEO_SIZE)
        if err:
            errors.append(f"Demo video: {err}")
        else:
            idea.product_demo_video_path = path

    if not is_draft and errors:
        return None, "; ".join(errors)

    idea.title = title
    idea.category = category
    idea.other_category = other_category
    idea.current_status = current_status
    idea.tags = form_data.get("tags", "")
    idea.target_market = target_market
    idea.summary = summary
    idea.problem_statement = problem_statement
    idea.proposed_solution = proposed_solution

    idea.full_name = full_name
    idea.email = email
    idea.contact_number = contact_number
    idea.founders = founders_raw
    idea.company_website = company_website or None
    idea.team_size = team_size
    idea.address = address
    idea.country = country

    idea.funding_goal = funding_goal
    idea.currency = currency
    idea.product_stage = product_stage
    idea.equity_offered = equity
    idea.funding_usage = funding_usage
    idea.expected_timeline = expected_timeline
    idea.revenue_status = revenue_status
    idea.monthly_revenue = monthly_revenue
    idea.existing_investors = existing_investors_raw
    idea.intellectual_property = intellectual_property
    idea.product_demo_url = product_demo_url or None

    if not is_draft:
        idea.status = "submitted"
        idea.is_draft = "false"
    else:
        idea.status = "draft"
        idea.is_draft = "true"

    idea.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(idea)
    return idea, None


def get_draft(db: Session, user_id: int) -> Idea | None:
    return (
        db.query(Idea)
        .filter(Idea.user_id == user_id, Idea.is_draft == "true")
        .order_by(Idea.updated_at.desc())
        .first()
    )


def get_admin_stats(db: Session) -> dict:
    """Gather admin dashboard statistics."""
    from models.creator_verification import CreatorVerification
    from models.investor_verification import InvestorVerification

    total_users = db.query(User).count()
    total_creators = db.query(User).filter(User.role == "creator").count()
    total_investors = db.query(User).filter(User.role == "investor").count()
    total_verified = db.query(User).filter(User.is_verified == True).count()

    pending_creator_verifications = db.query(CreatorVerification).filter(
        CreatorVerification.status == "pending"
    ).count()

    pending_investor_verifications = db.query(InvestorVerification).filter(
        InvestorVerification.status == "pending"
    ).count()

    total_pending_verifications = pending_creator_verifications + pending_investor_verifications
    active_users = db.query(User).filter(User.is_active == True).count()

    total_ideas = db.query(Idea).filter(Idea.is_draft == "false").count()

    creator_percent = (total_creators / total_users * 100) if total_users else 0
    investor_percent = (total_investors / total_users * 100) if total_users else 0
    verified_percent = (total_verified / total_users * 100) if total_users else 0

    return {
        "total_users": total_users,
        "total_creators": total_creators,
        "total_investors": total_investors,
        "total_verified": total_verified,
        "pending_creator_verifications": pending_creator_verifications,
        "pending_investor_verifications": pending_investor_verifications,
        "total_pending_verifications": total_pending_verifications,
        "active_users": active_users,
        "total_ideas": total_ideas,
        "creator_percent": creator_percent,
        "investor_percent": investor_percent,
        "verified_percent": verified_percent,
    }
