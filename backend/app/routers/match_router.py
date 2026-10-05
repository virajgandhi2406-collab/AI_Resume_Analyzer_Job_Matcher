from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.resume import Resume
from app.models.job import Job
from app.models.match import MatchResult
from app.schemas.match_schema import MatchRequest, MatchResponse, BatchMatchResponse
from app.services.job_matcher_service import JobMatcherService
from app.services.sample_data_service import seed_sample_jobs

router = APIRouter(prefix="/match", tags=["Job Matching & Compatibility Engine"])

@router.post("/match-single", response_model=MatchResponse)
def match_single(req: MatchRequest, db: Session = Depends(get_db)):
    # 1. Retrieve resume
    resume_text = req.resume_text or ""
    resume_skills = []
    
    if req.resume_id:
        resume = db.query(Resume).filter(Resume.id == req.resume_id).first()
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
        resume_text = resume.raw_text
        resume_skills = resume.extracted_skills or []

    if not resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either valid 'resume_id' or 'resume_text' must be provided."
        )

    # 2. Retrieve job or custom JD
    job = None
    job_title = req.job_title or "Target Role"
    job_description = req.job_description or ""
    job_required_skills = None

    if req.job_id:
        job = db.query(Job).filter(Job.id == req.job_id).first()
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
        job_title = job.title
        job_description = job.description
        job_required_skills = job.required_skills

    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either valid 'job_id' or 'job_description' must be provided."
        )

    # 3. Match calculation
    match_result_data = JobMatcherService.match_resume_to_job(
        resume_text=resume_text,
        resume_skills=resume_skills,
        job_title=job_title,
        job_description=job_description,
        job_required_skills=job_required_skills
    )

    # 4. Save to DB if both resume_id and job_id exist
    saved_match_id = None
    if req.resume_id and req.job_id:
        # Check existing match
        match_record = db.query(MatchResult).filter(
            MatchResult.resume_id == req.resume_id,
            MatchResult.job_id == req.job_id
        ).first()

        if not match_record:
            match_record = MatchResult(
                resume_id=req.resume_id,
                job_id=req.job_id,
                match_score=match_result_data["match_score"],
                skills_match_score=match_result_data["skills_match_score"],
                experience_match_score=match_result_data["experience_match_score"],
                semantic_similarity_score=match_result_data["semantic_similarity_score"],
                matched_skills=match_result_data["matched_skills"],
                missing_critical_skills=match_result_data["missing_critical_skills"],
                missing_nice_to_have=match_result_data["missing_nice_to_have"],
                fit_summary=match_result_data["fit_summary"],
                strengths_for_job=match_result_data["strengths_for_job"],
                tailored_recommendations=match_result_data["tailored_recommendations"],
                interview_focus_areas=match_result_data["interview_focus_areas"]
            )
            db.add(match_record)
        else:
            match_record.match_score = match_result_data["match_score"]
            match_record.skills_match_score = match_result_data["skills_match_score"]
            match_record.matched_skills = match_result_data["matched_skills"]
            match_record.missing_critical_skills = match_result_data["missing_critical_skills"]
            
        db.commit()
        db.refresh(match_record)
        saved_match_id = match_record.id

    return MatchResponse(
        id=saved_match_id,
        resume_id=req.resume_id,
        job_id=req.job_id,
        match_score=match_result_data["match_score"],
        skills_match_score=match_result_data["skills_match_score"],
        experience_match_score=match_result_data["experience_match_score"],
        semantic_similarity_score=match_result_data["semantic_similarity_score"],
        matched_skills=match_result_data["matched_skills"],
        missing_critical_skills=match_result_data["missing_critical_skills"],
        missing_nice_to_have=match_result_data["missing_nice_to_have"],
        fit_summary=match_result_data["fit_summary"],
        strengths_for_job=match_result_data["strengths_for_job"],
        tailored_recommendations=match_result_data["tailored_recommendations"],
        interview_focus_areas=match_result_data["interview_focus_areas"],
        job_details=job
    )

@router.post("/batch-match/{resume_id}", response_model=BatchMatchResponse)
def batch_match_all_jobs(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    jobs = db.query(Job).filter(Job.is_active == True).all()
    if not jobs:
        seed_sample_jobs(db)
        jobs = db.query(Job).filter(Job.is_active == True).all()

    ranked = []
    for job in jobs:
        match_data = JobMatcherService.match_resume_to_job(
            resume_text=resume.raw_text,
            resume_skills=resume.extracted_skills or [],
            job_title=job.title,
            job_description=job.description,
            job_required_skills=job.required_skills
        )
        ranked.append(
            MatchResponse(
                resume_id=resume.id,
                job_id=job.id,
                match_score=match_data["match_score"],
                skills_match_score=match_data["skills_match_score"],
                experience_match_score=match_data["experience_match_score"],
                semantic_similarity_score=match_data["semantic_similarity_score"],
                matched_skills=match_data["matched_skills"],
                missing_critical_skills=match_data["missing_critical_skills"],
                missing_nice_to_have=match_data["missing_nice_to_have"],
                fit_summary=match_data["fit_summary"],
                strengths_for_job=match_data["strengths_for_job"],
                tailored_recommendations=match_data["tailored_recommendations"],
                interview_focus_areas=match_data["interview_focus_areas"],
                job_details=job
            )
        )

    # Sort descending by match score
    ranked.sort(key=lambda x: x.match_score, reverse=True)

    return BatchMatchResponse(
        resume_id=resume.id,
        total_jobs_evaluated=len(jobs),
        ranked_jobs=ranked
    )
