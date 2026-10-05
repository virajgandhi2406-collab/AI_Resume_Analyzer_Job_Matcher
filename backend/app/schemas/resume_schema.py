from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class BulletImprovement(BaseModel):
    original: str
    improved: str
    reason: str
    impact_category: Optional[str] = "Impact & Metrics"

class ScoreBreakdown(BaseModel):
    keywords: float = 0.0
    formatting: float = 0.0
    impact_metrics: float = 0.0
    section_completeness: float = 0.0
    overall: float = 0.0

class ResumeBase(BaseModel):
    filename: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    candidate_location: Optional[str] = None
    candidate_linkedin: Optional[str] = None
    candidate_github: Optional[str] = None

class ResumeCreate(ResumeBase):
    raw_text: str
    parsed_sections: Dict[str, Any] = {}
    ats_score: float = 0.0
    score_breakdown: Dict[str, float] = {}
    extracted_skills: List[str] = []
    hard_skills: List[str] = []
    soft_skills: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    bullet_improvements: List[Dict[str, str]] = []

class ResumeResponse(ResumeBase):
    id: int
    user_id: Optional[int] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    raw_text: str
    parsed_sections: Dict[str, Any] = {}
    ats_score: float = 0.0
    score_breakdown: Dict[str, Any] = {}
    extracted_skills: List[str] = []
    hard_skills: List[str] = []
    soft_skills: List[str] = []
    action_verb_score: Optional[float] = 0.0
    quantifiable_metrics_count: Optional[int] = 0
    strengths: List[str] = []
    weaknesses: List[str] = []
    bullet_improvements: List[Dict[str, Any]] = []
    created_at: datetime

    class Config:
        from_attributes = True

class ResumeAnalysisRequest(BaseModel):
    raw_text: Optional[str] = None
    target_job_title: Optional[str] = None
    ai_provider: Optional[str] = "auto"
