
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from backend.app.db.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    preferred_roles = Column(String(500), nullable=True)

    preferred_locations = Column(String(500), nullable=True)

    min_salary = Column(Integer, nullable=True)

    employment_type = Column(String(100), nullable=True)

    work_mode = Column(String(50), nullable=True)

    user = relationship("User", back_populates="preferences")
