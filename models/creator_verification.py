from sqlalchemy import Column, Integer, String, ForeignKey
from database.database import Base

class CreatorVerification(Base):
    __tablename__ = "creator_verifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    full_name = Column(String(150), nullable=False)

    phone = Column(String(30), nullable=False)

    gov_id = Column(String(50), nullable=False)

    linkedin_id = Column(String(300), nullable=False)
    
    present_address = Column(String(500), nullable=False)


    status = Column(String(20), default="pending", nullable=False)