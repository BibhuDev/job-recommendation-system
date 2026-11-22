
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.app.models.job import Job


def get_jobs(db: Session, skip: int = 0, limit: int = 20):
    return (
        db.query(Job)
        .filter(Job.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_job_by_id(db: Session, job_id: int):
    return (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.is_active.is_(True)
        )
        .first()
    )


def create_job(db: Session, job_data: dict):
    job = Job(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def search_jobs(
    db: Session,
    query: str,
    skip: int = 0,
    limit: int = 20
):
    search_term = f"%{query.strip()}%"

    return (
        db.query(Job)
        .filter(
            Job.is_active.is_(True),
            or_(
                Job.title.ilike(search_term),
                Job.company.ilike(search_term),
                Job.location.ilike(search_term),
                Job.description.ilike(search_term),
                Job.required_skills.ilike(search_term),
                Job.experience_level.ilike(search_term),
                Job.employment_type.ilike(search_term)
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
