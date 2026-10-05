from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.job import Job
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse
from app.services.sample_data_service import seed_sample_jobs, SAMPLE_JOBS
from app.services.nlp_engine import NLPEngine

router = APIRouter(prefix="/jobs", tags=["Jobs & Opportunities"])

@router.get("/", response_model=List[JobResponse])
def get_jobs(
    search: Optional[str] = Query(None, description="Search by title, company, or keyword"),
    location: Optional[str] = Query(None),
    workplace_type: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Job).filter(Job.is_active == True)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Job.title.ilike(search_pattern),
                Job.company.ilike(search_pattern),
                Job.description.ilike(search_pattern)
            )
        )
        
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
        
    if workplace_type:
        query = query.filter(Job.workplace_type.ilike(f"%{workplace_type}%"))
        
    if experience_level:
        query = query.filter(Job.experience_level.ilike(f"%{experience_level}%"))

    jobs = query.order_by(Job.created_at.desc()).limit(limit).all()
    
    # Auto-seed if empty
    if not jobs and not search:
        seed_sample_jobs(db)
        jobs = db.query(Job).order_by(Job.created_at.desc()).limit(limit).all()
        
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job vacancy not found.")
    return job

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    # Auto-extract required skills if empty
    req_skills = job_in.required_skills
    if not req_skills:
        extracted = NLPEngine.extract_skills(f"{job_in.title} {job_in.description}")
        req_skills = extracted.get("hard_skills", [])

    job = Job(
        title=job_in.title,
        company=job_in.company,
        logo_url=job_in.logo_url,
        location=job_in.location or "Remote",
        job_type=job_in.job_type or "Full-time",
        workplace_type=job_in.workplace_type or "Remote",
        experience_level=job_in.experience_level or "Mid-Level",
        min_experience_years=job_in.min_experience_years or 2,
        salary_range=job_in.salary_range or "$100k - $140k",
        description=job_in.description,
        responsibilities=job_in.responsibilities or [],
        requirements=job_in.requirements or [],
        required_skills=req_skills,
        preferred_skills=job_in.preferred_skills or [],
        industry=job_in.industry or "Technology",
        source="User Posted",
        is_active=True
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.post("/seed", response_model=List[JobResponse])
def seed_jobs_endpoint(db: Session = Depends(get_db)):
    """Seed sample industry jobs into the database"""
    for job_data in SAMPLE_JOBS:
        existing = db.query(Job).filter(Job.title == job_data["title"], Job.company == job_data["company"]).first()
        if not existing:
            job = Job(**job_data)
            db.add(job)
    db.commit()
    return db.query(Job).all()

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully", "id": job_id}
