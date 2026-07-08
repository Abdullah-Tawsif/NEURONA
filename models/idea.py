from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from database.database import Base


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(String(20), unique=True, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Phase 1 — Basic Information
    title = Column(String(300), nullable=False)
    category = Column(String(500), nullable=False)
    other_category = Column(String(100), nullable=True)
    current_status = Column(String(500), nullable=False)
    tags = Column(Text, nullable=True)
    target_market = Column(String(500), nullable=False)
    summary = Column(Text, nullable=False)
    problem_statement = Column(Text, nullable=False)
    proposed_solution = Column(Text, nullable=False)

    # Phase 2 — Information & Contact
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    contact_number = Column(String(50), nullable=False)
    founders = Column(Text, nullable=False)
    company_website = Column(String(500), nullable=True)
    team_size = Column(Integer, nullable=False)
    address = Column(Text, nullable=False)
    country = Column(String(100), nullable=False)

    # Phase 3 — Funding & Attachments
    funding_goal = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    product_stage = Column(String(50), nullable=False)
    equity_offered = Column(Float, nullable=False)
    funding_usage = Column(Text, nullable=False)
    expected_timeline = Column(String(50), nullable=False)
    revenue_status = Column(String(50), nullable=False)
    monthly_revenue = Column(Float, nullable=True)
    existing_investors = Column(Text, nullable=True)
    business_plan_path = Column(String(500), nullable=False)
    product_images = Column(Text, nullable=False)
    intellectual_property = Column(String(500), nullable=True)
    ip_document_paths = Column(Text, nullable=True)
    product_demo_url = Column(String(500), nullable=True)
    product_demo_video_path = Column(String(500), nullable=True)

    # Metadata
    status = Column(String(20), default="submitted", nullable=False)
    is_draft = Column(String(10), default="false", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
