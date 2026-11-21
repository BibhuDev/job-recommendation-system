
from sqlalchemy.orm import Session
from backend.app.models.job import Job


def get_jobs(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Job).filter(
        Job.is_active == True
    ).offset(skip).limit(limit).all()


def get_job_by_id(db: Session, job_id: int):
    return db.query(Job).filter(
        Job.id == job_id,
        Job.is_active == True
    ).first()


def create_job(db: Session, job_data: dict):
    job = Job(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
