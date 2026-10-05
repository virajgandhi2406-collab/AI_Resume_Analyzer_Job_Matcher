from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel

# --- Cover Letter ---
class CoverLetterRequest(BaseModel):
    resume_id: Optional[int] = None
    resume_text: Optional[str] = None
    job_id: Optional[int] = None
    job_description: Optional[str] = None
    job_title: str
    company_name: str
    tone: Optional[str] = "professional" # professional, enthusiastic, executive, technical, confident
    custom_notes: Optional[str] = None
    ai_provider: Optional[str] = "auto"

class CoverLetterResponse(BaseModel):
    job_title: str
    company_name: str
    tone: str
    cover_letter: str
    key_selling_points: List[str] = []

# --- Interview Prep ---
class InterviewPrepRequest(BaseModel):
    resume_id: Optional[int] = None
    resume_text: Optional[str] = None
    job_title: str
    job_description: Optional[str] = None
    question_count: Optional[int] = 5
    ai_provider: Optional[str] = "auto"

class InterviewQuestion(BaseModel):
    category: str # Behavioral (STAR), Technical, Role-Specific, Situational
    question: str
    why_asked: str
    recommended_star_answer: str
    resume_talking_point: str

class InterviewPrepResponse(BaseModel):
    job_title: str
    questions: List[InterviewQuestion]

# --- Bullet Optimizer ---
class BulletOptimizerRequest(BaseModel):
    bullet_points: List[str]
    target_role: Optional[str] = None
    ai_provider: Optional[str] = "auto"

class OptimizedBullet(BaseModel):
    original: str
    improved: str
    impact_level: str # High, Very High
    action_verb_used: str
    metric_added: bool
    explanation: str

class BulletOptimizerResponse(BaseModel):
    optimized_bullets: List[OptimizedBullet]

# --- Career Roadmap ---
class CareerRoadmapRequest(BaseModel):
    current_skills: List[str]
    target_role: str
    ai_provider: Optional[str] = "auto"

class LearningStep(BaseModel):
    phase: str # Month 1, Month 2, etc.
    title: str
    skills_to_learn: List[str]
    recommended_projects: List[str]
    suggested_resources: List[str]

class CareerRoadmapResponse(BaseModel):
    target_role: str
    estimated_timeline: str
    milestones: List[LearningStep]

# --- Application Tracker ---
class ApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    location: Optional[str] = "Remote"
    salary_target: Optional[str] = None
    status: Optional[str] = "WISHLIST" # WISHLIST, APPLIED, INTERVIEWING, OFFER, REJECTED
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    match_score: Optional[Union[float, int]] = 0
    notes: Optional[str] = None
    job_url: Optional[str] = None
    job_id: Optional[int] = None
    resume_id: Optional[int] = None

class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    salary_target: Optional[str] = None
    status: Optional[str] = None
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    match_score: Optional[Union[float, int]] = None
    notes: Optional[str] = None
    job_url: Optional[str] = None

class ApplicationResponse(ApplicationCreate):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
