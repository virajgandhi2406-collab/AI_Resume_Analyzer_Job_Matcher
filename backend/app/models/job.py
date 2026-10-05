from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    logo_url = Column(String(512), nullable=True)
    location = Column(String(255), default="Remote")
    job_type = Column(String(50), default="Full-time") # Full-time, Part-time, Contract, Internship
    workplace_type = Column(String(50), default="Remote") # Remote, Hybrid, On-site
    
    experience_level = Column(String(50), default="Mid-Level") # Entry, Mid-Level, Senior, Lead
    min_experience_years = Column(Integer, default=2)
    salary_range = Column(String(100), nullable=True) # e.g. "$110,000 - $145,000"
    
    description = Column(Text, nullable=False)
    responsibilities = Column(JSON, default=list)
    requirements = Column(JSON, default=list)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    
    industry = Column(String(100), default="Technology")
    source = Column(String(100), default="System")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    matches = relationship("MatchResult", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job")
