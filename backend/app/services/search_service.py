
import re

from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from backend.app.models.job import Job


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
