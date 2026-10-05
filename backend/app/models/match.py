from datetime import datetime
from sqlalchemy import Column, Integer, Float, JSON, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Overall and sub-scores (0-100)
    match_score = Column(Float, nullable=False, default=0.0)
    skills_match_score = Column(Float, default=0.0)
    experience_match_score = Column(Float, default=0.0)
    semantic_similarity_score = Column(Float, default=0.0)
    
    # Deep Breakdown
    matched_skills = Column(JSON, default=list)       # List of skills found in both
    missing_critical_skills = Column(JSON, default=list) # Skills required by JD but missing in resume
    missing_nice_to_have = Column(JSON, default=list) # Preferred skills missing
    
    # AI Qualitative Assessment & Gap Analysis
    fit_summary = Column(Text, nullable=True)
    strengths_for_job = Column(JSON, default=list)
    tailored_recommendations = Column(JSON, default=list) # Bullet items candidate should add/rephrase
    interview_focus_areas = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="matches")
    job = relationship("Job", back_populates="matches")
