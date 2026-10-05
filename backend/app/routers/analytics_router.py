from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter

from app.database import get_db
from app.models.resume import Resume
from app.models.job import Job
from app.models.match import MatchResult
from app.models.application import Application
from app.services.sample_data_service import seed_sample_jobs

router = APIRouter(prefix="/analytics", tags=["Dashboard & Analytics"])

@router.get("/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    # Ensure sample jobs if empty
    if db.query(Job).count() == 0:
        seed_sample_jobs(db)

    # Resume Stats
    total_resumes = db.query(Resume).count()
    avg_score_res = db.query(func.avg(Resume.ats_score)).scalar() or 0.0
    
    # Jobs & Match Stats
    total_jobs = db.query(Job).filter(Job.is_active == True).count()
    total_matches = db.query(MatchResult).count()
    
    # Application Funnel
    applications = db.query(Application).all()
    pipeline_counts = {
        "WISHLIST": 0,
        "APPLIED": 0,
        "INTERVIEWING": 0,
        "OFFER": 0,
        "REJECTED": 0
    }
    for app in applications:
        status_key = app.status.upper() if app.status else "WISHLIST"
        if status_key in pipeline_counts:
            pipeline_counts[status_key] += 1
            
    # Skill frequency across all jobs
    jobs = db.query(Job).all()
    skill_counter = Counter()
    for j in jobs:
        if j.required_skills:
            for s in j.required_skills:
                skill_counter[s] += 1
                
    top_skills_in_demand = [
        {"skill": skill, "count": count}
        for skill, count in skill_counter.most_common(8)
    ]

    # Recent resumes
    recent_resumes = db.query(Resume).order_by(Resume.created_at.desc()).limit(5).all()
    recent_resumes_data = [
        {
            "id": r.id,
            "filename": r.filename,
            "candidate_name": r.candidate_name,
            "ats_score": r.ats_score,
            "created_at": r.created_at
        }
        for r in recent_resumes
    ]

    return {
        "total_resumes_analyzed": total_resumes,
        "average_ats_score": round(float(avg_score_res), 1),
        "total_active_jobs": total_jobs,
        "total_matches_generated": total_matches,
        "pipeline_counts": pipeline_counts,
        "top_skills_in_demand": top_skills_in_demand,
        "recent_resumes": recent_resumes_data
    }
