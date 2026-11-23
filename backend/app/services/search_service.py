
import re

from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from backend.app.models.job import Job
from backend.app.services.embedding_service import generate_query_embedding


def tokenize(text: str) -> list[str]:
    """Convert text into lowercase word tokens."""
    return re.findall(r"\b\w+\b", text.lower())


def bm25_search(
    db: Session,
    query: str,
    skip: int = 0,
    limit: int = 20
):
    jobs = (
        db.query(Job)
        .filter(Job.is_active.is_(True))
        .all()
    )

    if not jobs:
        return []

    # Build a searchable document for each job.
    documents = []

    for job in jobs:
        document = " ".join([
            job.title or "",
            job.company or "",
            job.location or "",
            job.description or "",
            job.required_skills or "",
            job.experience_level or "",
            job.employment_type or ""
        ])

        documents.append(tokenize(document))

    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    # Build the BM25 ranking model.
    bm25 = BM25Okapi(documents)

    # Calculate relevance scores.
    scores = bm25.get_scores(query_tokens)

    # Sort jobs by descending relevance score.
    ranked_jobs = sorted(
        zip(jobs, scores),
        key=lambda item: item[1],
        reverse=True
    )

    # Exclude jobs with no matching terms.
    ranked_jobs = [
        job for job, score in ranked_jobs
        if score > 0
    ]

    return ranked_jobs[skip:skip + limit]

def semantic_search(
    db,
    query: str,
    skip: int = 0,
    limit: int = 20
):
    query_embedding = generate_query_embedding(query)

    results = (
        db.query(Job)
        .filter(
            Job.is_active.is_(True),
            Job.embedding.is_not(None)
        )
        .order_by(
            Job.embedding.cosine_distance(query_embedding)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return results


def hybrid_search(
    db,
    query: str,
    skip: int = 0,
    limit: int = 20
):
    """
    Combine BM25 and semantic rankings using
    Reciprocal Rank Fusion (RRF).
    """

    candidate_limit = 100

    # Retrieve ranked results from both search methods.
    bm25_results = bm25_search(
        db, query, skip=0, limit=candidate_limit
    )

    semantic_results = semantic_search(
        db, query, skip=0, limit=candidate_limit
    )

    # Store combined scores for each job.
    scores = {}
    jobs_by_id = {}

    rrf_constant = 60

    # Add BM25 ranking scores.
    for rank, job in enumerate(bm25_results, start=1):
        scores[job.id] = scores.get(job.id, 0) + (
            1 / (rrf_constant + rank)
        )
        jobs_by_id[job.id] = job

    # Add semantic ranking scores.
    for rank, job in enumerate(semantic_results, start=1):
        scores[job.id] = scores.get(job.id, 0) + (
            1 / (rrf_constant + rank)
        )
        jobs_by_id[job.id] = job

    # Sort jobs by their combined RRF scores.
    ranked_ids = sorted(
        scores,
        key=lambda job_id: scores[job_id],
        reverse=True
    )

    ranked_jobs = [
        jobs_by_id[job_id]
        for job_id in ranked_ids
    ]

    return ranked_jobs[skip:skip + limit]
