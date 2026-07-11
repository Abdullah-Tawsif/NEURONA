from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from database.database import Base


class IdeaDeleteRequest(Base):
    __tablename__ = "idea_delete_requests"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed_at = Column(DateTime, nullable=True)


class IdeaAdminNote(Base):
    __tablename__ = "idea_admin_notes"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False, index=True)
    admin_user_id = Column(Integer, nullable=True)
    note = Column(Text, nullable=False)
    note_type = Column(String(30), nullable=False, default="general")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
