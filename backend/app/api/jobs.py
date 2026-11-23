from backend.app.services.search_service import bm25_search
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.services.search_service import semantic_search
from backend.app.services.search_service import hybrid_search
from backend.app.db.database import get_db
from backend.app.services.job_service import (
    get_jobs,
    get_job_by_id,
    search_jobs
)
from backend.app.schemas.job import JobResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=list[JobResponse])
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_jobs(db, skip=skip, limit=limit)


@router.get("/search", response_model=list[JobResponse])
def search_job_listings(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return search_jobs(
        db,
        query=q,
        skip=skip,
        limit=limit
    )


@router.get("/search/bm25", response_model=list[JobResponse])
def search_jobs_bm25(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return bm25_search(
        db,
        query=q,
        skip=skip,
        limit=limit
    )

@router.get("/search/semantic", response_model=list[JobResponse])
def search_jobs_semantic(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return semantic_search(
        db,
        query=q,
        skip=skip,
        limit=limit
    )


@router.get("/search/hybrid", response_model=list[JobResponse])
def search_jobs_hybrid(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return hybrid_search(
        db,
        query=q,
        skip=skip,
        limit=limit
    )


@router.get("/{job_id}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db)):
    job = get_job_by_id(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job
