import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.resume import Resume
from app.schemas.resume_schema import ResumeResponse, ResumeAnalysisRequest
from app.services.resume_parser import ResumeParser
from app.services.nlp_engine import NLPEngine
from app.services.resume_optimizer import ResumeOptimizerService
from app.utils.pdf_generator import generate_pdf_report
from app.config import settings

router = APIRouter(prefix="/resumes", tags=["Resumes & ATS Analyzer"])

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    ai_provider: str = Form("auto"),
    db: Session = Depends(get_db)
):
    # Validate extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{file_ext}'. Please upload PDF, DOCX, or TXT."
        )

    # Save to disk
    file_path = settings.UPLOAD_DIR / f"{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Parse text & contact details
        raw_text = ResumeParser.extract_text(str(file_path))
        if not raw_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract readable text from the uploaded document. Please check the file."
            )

        contact = ResumeParser.extract_contact_info(raw_text)
        sections = ResumeParser.extract_sections(raw_text)

        # 2. NLP Engine Analysis
        skills_data = NLPEngine.extract_skills(raw_text)
        ats_score, breakdown, strengths, weaknesses = NLPEngine.calculate_ats_score(
            raw_text, sections, skills_data
        )
        impact = NLPEngine.analyze_action_verbs_and_metrics(raw_text)

        # 3. Generate initial bullet improvements
        # Extract potential bullet lines
        sample_bullets = [
            line.strip().lstrip("-•* ") for line in raw_text.splitlines()
            if 30 < len(line.strip()) < 160 and not line.strip().endswith(":")
        ][:3]
        
        if not sample_bullets:
            sample_bullets = ["Developed web applications and handled feature requests from product team."]
            
        bullet_improvements = await ResumeOptimizerService.optimize_bullets(
            sample_bullets,
            target_role="Software Engineer",
            provider=ai_provider
        )

        # 4. Save to Database
        resume_record = Resume(
            filename=file.filename,
            file_path=str(file_path),
            file_type=file_ext.replace(".", ""),
            candidate_name=contact.get("name") or "Candidate",
            candidate_email=contact.get("email"),
            candidate_phone=contact.get("phone"),
            candidate_linkedin=contact.get("linkedin"),
            candidate_github=contact.get("github"),
            raw_text=raw_text,
            parsed_sections=sections,
            ats_score=ats_score,
            score_breakdown=breakdown,
            extracted_skills=skills_data.get("all_skills", []),
            hard_skills=skills_data.get("hard_skills", []),
            soft_skills=skills_data.get("soft_skills", []),
            action_verb_score=float(impact.get("action_verbs_count", 0)),
            quantifiable_metrics_count=impact.get("metrics_count", 0),
            strengths=strengths,
            weaknesses=weaknesses,
            bullet_improvements=bullet_improvements
        )

        db.add(resume_record)
        db.commit()
        db.refresh(resume_record)

        return resume_record

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume analysis failed: {str(e)}"
        )

@router.post("/analyze-text", response_model=ResumeResponse)
async def analyze_raw_text(
    req: ResumeAnalysisRequest,
    db: Session = Depends(get_db)
):
    if not req.raw_text or not req.raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text content is required."
        )

    contact = ResumeParser.extract_contact_info(req.raw_text)
    sections = ResumeParser.extract_sections(req.raw_text)
    skills_data = NLPEngine.extract_skills(req.raw_text)
    
    ats_score, breakdown, strengths, weaknesses = NLPEngine.calculate_ats_score(
        req.raw_text, sections, skills_data
    )
    impact = NLPEngine.analyze_action_verbs_and_metrics(req.raw_text)

    sample_bullets = [
        line.strip().lstrip("-•* ") for line in req.raw_text.splitlines()
        if 30 < len(line.strip()) < 160
    ][:3]
    if not sample_bullets:
        sample_bullets = ["Implemented new software modules and collaborated on bug resolutions."]

    bullet_improvements = await ResumeOptimizerService.optimize_bullets(
        sample_bullets,
        target_role=req.target_job_title or "Software Engineer",
        provider=req.ai_provider or "auto"
    )

    resume_record = Resume(
        filename="Pasted_Resume.txt",
        file_path=None,
        file_type="txt",
        candidate_name=contact.get("name") or "Candidate",
        candidate_email=contact.get("email"),
        candidate_phone=contact.get("phone"),
        candidate_linkedin=contact.get("linkedin"),
        candidate_github=contact.get("github"),
        raw_text=req.raw_text,
        parsed_sections=sections,
        ats_score=ats_score,
        score_breakdown=breakdown,
        extracted_skills=skills_data.get("all_skills", []),
        hard_skills=skills_data.get("hard_skills", []),
        soft_skills=skills_data.get("soft_skills", []),
        action_verb_score=float(impact.get("action_verbs_count", 0)),
        quantifiable_metrics_count=impact.get("metrics_count", 0),
        strengths=strengths,
        weaknesses=weaknesses,
        bullet_improvements=bullet_improvements
    )

    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    return resume_record

@router.get("/", response_model=List[ResumeResponse])
def get_all_resumes(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Resume).order_by(Resume.created_at.desc()).limit(limit).all()

@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
    return resume

@router.get("/{resume_id}/export-pdf")
def export_resume_pdf(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    resume_dict = {
        "candidate_name": resume.candidate_name,
        "ats_score": resume.ats_score,
        "score_breakdown": resume.score_breakdown,
        "extracted_skills": resume.extracted_skills,
        "hard_skills": resume.hard_skills,
        "soft_skills": resume.soft_skills,
        "strengths": resume.strengths,
        "weaknesses": resume.weaknesses,
        "bullet_improvements": resume.bullet_improvements
    }

    pdf_buffer = generate_pdf_report(resume_dict)
    
    filename = f"ATS_Scorecard_{resume.candidate_name or 'Candidate'}_{resume.id}.pdf".replace(" ", "_")
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.delete("/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
    
    if resume.file_path and os.path.exists(resume.file_path):
        try:
            os.remove(resume.file_path)
        except Exception:
            pass
            
    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted successfully", "id": resume_id}
