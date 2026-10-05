from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.resume import Resume
from app.models.job import Job
from app.schemas.tools_schema import (
    CoverLetterRequest, CoverLetterResponse,
    InterviewPrepRequest, InterviewPrepResponse,
    BulletOptimizerRequest, BulletOptimizerResponse,
    CareerRoadmapRequest, CareerRoadmapResponse, LearningStep
)
from app.services.cover_letter_service import CoverLetterService
from app.services.interview_prep_service import InterviewPrepService
from app.services.resume_optimizer import ResumeOptimizerService

router = APIRouter(prefix="/ai-tools", tags=["AI Copilot Tools"])

@router.post("/cover-letter", response_model=CoverLetterResponse)
async def generate_tailored_cover_letter(req: CoverLetterRequest, db: Session = Depends(get_db)):
    resume_text = req.resume_text or ""
    candidate_name = "Candidate"
    
    if req.resume_id:
        resume = db.query(Resume).filter(Resume.id == req.resume_id).first()
        if resume:
            resume_text = resume.raw_text
            candidate_name = resume.candidate_name or "Candidate"

    job_desc = req.job_description or ""
    if req.job_id:
        job = db.query(Job).filter(Job.id == req.job_id).first()
        if job:
            job_desc = job.description

    result = await CoverLetterService.generate_cover_letter(
        candidate_name=candidate_name,
        resume_text=resume_text,
        job_title=req.job_title,
        company_name=req.company_name,
        job_description=job_desc,
        tone=req.tone or "professional",
        custom_notes=req.custom_notes or "",
        provider=req.ai_provider or "auto"
    )

    return CoverLetterResponse(**result)

@router.post("/interview-prep", response_model=InterviewPrepResponse)
async def generate_interview_prep(req: InterviewPrepRequest, db: Session = Depends(get_db)):
    resume_text = req.resume_text or ""
    if req.resume_id:
        resume = db.query(Resume).filter(Resume.id == req.resume_id).first()
        if resume:
            resume_text = resume.raw_text

    result = await InterviewPrepService.generate_interview_prep(
        resume_text=resume_text,
        job_title=req.job_title,
        job_description=req.job_description or "",
        question_count=req.question_count or 5,
        provider=req.ai_provider or "auto"
    )

    return InterviewPrepResponse(**result)

@router.post("/optimize-bullets", response_model=BulletOptimizerResponse)
async def optimize_resume_bullets(req: BulletOptimizerRequest):
    if not req.bullet_points:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one bullet point required.")

    optimized = await ResumeOptimizerService.optimize_bullets(
        bullet_points=req.bullet_points,
        target_role=req.target_role or "Software Engineer",
        provider=req.ai_provider or "auto"
    )

    return BulletOptimizerResponse(optimized_bullets=optimized)

@router.post("/career-roadmap", response_model=CareerRoadmapResponse)
async def generate_career_roadmap(req: CareerRoadmapRequest):
    # Generates a personalized upskilling path
    target = req.target_role
    milestones = [
        LearningStep(
            phase="Phase 1: Core Fundamentals & Frameworks",
            title=f"Master Modern {target} Essentials",
            skills_to_learn=[s for s in ["System Design", "Microservices", "Docker"] if s not in req.current_skills][:3],
            recommended_projects=[
                f"Build an end-to-end full-stack scalable service for {target}",
                "Implement distributed caching and database indexing"
            ],
            suggested_resources=[
                "Official Framework Documentation",
                "Designing Data-Intensive Applications (Book)"
            ]
        ),
        LearningStep(
            phase="Phase 2: Cloud, DevOps & Production Readiness",
            title="Production Infrastructure & CI/CD",
            skills_to_learn=["Kubernetes", "AWS / Cloud", "GitHub Actions CI/CD"],
            recommended_projects=[
                "Deploy a multi-container cluster with automated health checks & monitoring",
                "Set up zero-downtime deployment pipeline"
            ],
            suggested_resources=[
                "Kubernetes in Action",
                "AWS Solutions Architect Handbook"
            ]
        ),
        LearningStep(
            phase="Phase 3: Portfolio & Interview Mastery",
            title="High-Impact Demonstration & System Architecture",
            skills_to_learn=["System Architecture", "STAR Interview Mastery", "Performance Profiling"],
            recommended_projects=[
                "Publish open-source benchmark repository with live documentation",
                "Write technical blog post detailing architectural trade-offs"
            ],
            suggested_resources=[
                "Grokking the System Design Interview",
                "LeetCode & Mock Interview Platforms"
            ]
        )
    ]

    return CareerRoadmapResponse(
        target_role=target,
        estimated_timeline="3 - 6 Months",
        milestones=milestones
    )
