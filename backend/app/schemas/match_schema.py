from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.job_schema import JobResponse

class MatchRequest(BaseModel):
    resume_id: Optional[int] = None
    resume_text: Optional[str] = None
    job_id: Optional[int] = None
    job_description: Optional[str] = None
    job_title: Optional[str] = None
    ai_provider: Optional[str] = "auto"

class MatchResponse(BaseModel):
    id: Optional[int] = None
    resume_id: Optional[int] = None
    job_id: Optional[int] = None
    match_score: float
    skills_match_score: float
    experience_match_score: float
    semantic_similarity_score: float
    matched_skills: List[str] = []
    missing_critical_skills: List[str] = []
    missing_nice_to_have: List[str] = []
    fit_summary: Optional[str] = None
    strengths_for_job: List[str] = []
    tailored_recommendations: List[str] = []
    interview_focus_areas: List[str] = []
    job_details: Optional[JobResponse] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BatchMatchResponse(BaseModel):
    resume_id: int
    total_jobs_evaluated: int
    ranked_jobs: List[MatchResponse]
