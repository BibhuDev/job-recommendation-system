
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Data accepted when creating a job
class JobCreate(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str | None = None
    required_skills: str | None = None
    experience_level: str | None = None
    employment_type: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    job_url: str | None = None
    posted_at: datetime | None = None


# Data returned by the API
class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    location: str | None
    description: str | None
    required_skills: str | None
    experience_level: str | None
    employment_type: str | None
    salary_min: int | None
    salary_max: int | None
    job_url: str | None
    is_active: bool
    posted_at: datetime | None
    created_at: datetime
