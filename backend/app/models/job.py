from pgvector.sqlalchemy import Vector

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean
)
from sqlalchemy.sql import func

from backend.app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    company = Column(String(255), nullable=False)

    location = Column(String(255), nullable=True)

    description = Column(Text, nullable=True)

    required_skills = Column(Text, nullable=True)

    experience_level = Column(String(100), nullable=True)

    employment_type = Column(String(100), nullable=True)

    salary_min = Column(Integer, nullable=True)

    salary_max = Column(Integer, nullable=True)

    job_url = Column(String(500), nullable=True, unique=True)

    is_active = Column(Boolean, default=True)

    posted_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    embedding = Column(Vector(384), nullable=True)
