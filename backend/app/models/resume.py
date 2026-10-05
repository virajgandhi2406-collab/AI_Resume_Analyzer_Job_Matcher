from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=True)
    file_type = Column(String(50), nullable=True) # pdf, docx, txt
    
    # Candidate Extracted Details
    candidate_name = Column(String(255), nullable=True)
    candidate_email = Column(String(255), nullable=True)
    candidate_phone = Column(String(100), nullable=True)
    candidate_location = Column(String(255), nullable=True)
    candidate_linkedin = Column(String(255), nullable=True)
    candidate_github = Column(String(255), nullable=True)
    
    # Resume Content
    raw_text = Column(Text, nullable=False)
    parsed_sections = Column(JSON, default=dict) # summary, experience, education, skills, projects, certifications
    
    # ATS & AI Analysis Metrics
    ats_score = Column(Float, default=0.0)
    score_breakdown = Column(JSON, default=dict) # {keywords: 85, format: 90, impact: 70, completeness: 95}
    extracted_skills = Column(JSON, default=list) # ["Python", "FastAPI", "React", "PostgreSQL", ...]
    hard_skills = Column(JSON, default=list)
    soft_skills = Column(JSON, default=list)
    
    # AI Suggestions & Feedback
    action_verb_score = Column(Float, default=0.0)
    quantifiable_metrics_count = Column(Integer, default=0)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    bullet_improvements = Column(JSON, default=list) # [{original: "...", improved: "...", reason: "..."}]
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resumes")
    matches = relationship("MatchResult", back_populates="resume", cascade="all, delete-orphan")
