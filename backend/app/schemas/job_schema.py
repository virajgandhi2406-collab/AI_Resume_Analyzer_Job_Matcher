from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    company: str
    logo_url: Optional[str] = None
    location: Optional[str] = "Remote"
    job_type: Optional[str] = "Full-time"
    workplace_type: Optional[str] = "Remote"
    experience_level: Optional[str] = "Mid-Level"
    min_experience_years: Optional[int] = 2
    salary_range: Optional[str] = "$100k - $130k"
    description: str
    responsibilities: Optional[List[str]] = []
    requirements: Optional[List[str]] = []
    required_skills: Optional[List[str]] = []
    preferred_skills: Optional[List[str]] = []
    industry: Optional[str] = "Technology"

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    workplace_type: Optional[str] = None
    experience_level: Optional[str] = None
    min_experience_years: Optional[int] = None
    salary_range: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    is_active: Optional[bool] = None

class JobResponse(JobBase):
    id: int
    source: Optional[str] = "System"
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class JobMatchSummary(JobResponse):
    match_score: Optional[float] = 0.0
    skills_match_score: Optional[float] = 0.0
    matched_skills: Optional[List[str]] = []
    missing_critical_skills: Optional[List[str]] = []
