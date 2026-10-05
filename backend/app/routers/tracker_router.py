from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.schemas.tools_schema import ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter(prefix="/tracker", tags=["Application Kanban Tracker"])

@router.get("/", response_model=List[ApplicationResponse])
def get_applications(
    status_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Application)
    if status_filter:
        query = query.filter(Application.status == status_filter.upper())
    return query.order_by(Application.updated_at.desc()).all()

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    app_record = Application(
        company_name=app_in.company_name,
        job_title=app_in.job_title,
        location=app_in.location or "Remote",
        salary_target=app_in.salary_target,
        status=(app_in.status or "WISHLIST").upper(),
        applied_date=app_in.applied_date or datetime.utcnow(),
        interview_date=app_in.interview_date,
        match_score=app_in.match_score or 0,
        notes=app_in.notes,
        job_url=app_in.job_url,
        job_id=app_in.job_id,
        resume_id=app_in.resume_id
    )
    db.add(app_record)
    db.commit()
    db.refresh(app_record)
    return app_record

@router.put("/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, app_in: ApplicationUpdate, db: Session = Depends(get_db)):
    app_record = db.query(Application).filter(Application.id == app_id).first()
    if not app_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")

    update_data = app_in.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"]:
        update_data["status"] = update_data["status"].upper()

    for key, value in update_data.items():
        setattr(app_record, key, value)

    app_record.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(app_record)
    return app_record

@router.delete("/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    app_record = db.query(Application).filter(Application.id == app_id).first()
    if not app_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")
    db.delete(app_record)
    db.commit()
    return {"message": "Application removed successfully", "id": app_id}
