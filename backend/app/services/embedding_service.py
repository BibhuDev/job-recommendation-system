
from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from backend.app.models.job import Job


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


def build_job_text(job: Job) -> str:
    """Combine relevant job fields into searchable text."""
    return " ".join(filter(None, [
        job.title,
        job.company,
        job.location,
        job.description,
        job.required_skills,
        job.experience_level,
        job.employment_type
    ]))


def generate_job_embeddings(db: Session, batch_size: int = 32) -> int:
    """Generate and save embeddings for jobs without embeddings."""

    jobs = (
        db.query(Job)
        .filter(
            Job.is_active.is_(True),
            Job.embedding.is_(None)
        )
        .all()
    )

    if not jobs:
        print("No jobs need embeddings.")
        return 0

    model = get_embedding_model()
    texts = [build_job_text(job) for job in jobs]

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    for job, embedding in zip(jobs, embeddings):
        job.embedding = embedding.tolist()

    db.commit()

    print(f"Successfully generated embeddings for {len(jobs)} jobs.")
    return len(jobs)

def generate_query_embedding(query: str) -> list[float]:
    """Convert a search query into a 384-dimensional vector."""
    model = get_embedding_model()

    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()