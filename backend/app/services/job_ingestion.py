import csv
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.models.job import Job


def parse_optional_int(value):
    value = (value or "").strip()
    return int(value) if value else None


def import_jobs_from_csv(db: Session, file_path: str):
    inserted = 0
    skipped = 0
    errors = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {"title", "company", "job_url"}

        if not required_columns.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"CSV must contain these columns: {required_columns}"
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                title = (row.get("title") or "").strip()
                company = (row.get("company") or "").strip()
                job_url = (row.get("job_url") or "").strip()

                if not title or not company or not job_url:
                    raise ValueError(
                        "Title, company, and job URL are required"
                    )

                existing = db.query(Job).filter(
                    Job.job_url == job_url
                ).first()

                if existing:
                    skipped += 1
                    continue

                posted_at_value = (row.get("posted_at") or "").strip()

                posted_at = (
                    datetime.fromisoformat(posted_at_value)
                    if posted_at_value
                    else None
                )

                job = Job(
                    title=title,
                    company=company,
                    location=(row.get("location") or "").strip() or None,
                    description=(row.get("description") or "").strip() or None,
                    required_skills=(
                        (row.get("required_skills") or "").strip() or None
                    ),
                    experience_level=(
                        (row.get("experience_level") or "").strip() or None
                    ),
                    employment_type=(
                        (row.get("employment_type") or "").strip() or None
                    ),
                    salary_min=parse_optional_int(row.get("salary_min")),
                    salary_max=parse_optional_int(row.get("salary_max")),
                    job_url=job_url,
                    posted_at=posted_at,
                )

                db.add(job)
                db.flush()
                inserted += 1

            except (ValueError, TypeError) as error:
                db.rollback()
                errors.append({
                    "row": row_number,
                    "error": str(error)
                })

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

    return {
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors
    }
