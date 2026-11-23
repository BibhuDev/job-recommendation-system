import json

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from backend.app.db.database import SessionLocal
from backend.app.services.search_service import hybrid_search


class JobSearchInput(BaseModel):
    query: str = Field(
        description="The job title, skills, technologies, or role the user is looking for."
    )


@tool(args_schema=JobSearchInput)
def search_jobs(query: str) -> str:
    """Search the job database using hybrid keyword and semantic search."""

    db = SessionLocal()

    try:
        jobs = hybrid_search(
            db=db,
            query=query,
            skip=0,
            limit=5
        )

        results = []

        for job in jobs:
            results.append({
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": (job.description or "")[:500],
                "required_skills": job.required_skills,
                "experience_level": job.experience_level,
                "employment_type": job.employment_type,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "job_url": job.job_url
            })

        if not results:
            return "No matching jobs were found."

        return json.dumps(results, ensure_ascii=False)

    except Exception as error:
        return f"Job search failed: {str(error)}"

    finally:
        db.close()


tools = [search_jobs]