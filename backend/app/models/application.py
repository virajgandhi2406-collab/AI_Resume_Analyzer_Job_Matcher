from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    location = Column(String(255), default="Remote")
    salary_target = Column(String(100), nullable=True)
    
    # Kanban Status: WISHLIST, APPLIED, INTERVIEWING, OFFER, REJECTED
    status = Column(String(50), default="WISHLIST", index=True)
    
    applied_date = Column(DateTime, nullable=True)
    interview_date = Column(DateTime, nullable=True)
    match_score = Column(Integer, default=0)
    
    notes = Column(Text, nullable=True)
    job_url = Column(String(512), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
