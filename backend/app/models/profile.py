
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.db.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    headline = Column(String(255), nullable=True)

    location = Column(String(150), nullable=True)

    experience_years = Column(Integer, default=0)

    skills = Column(Text, nullable=True)

    education = Column(Text, nullable=True)

    bio = Column(Text, nullable=True)

    user = relationship("User", back_populates="profile")
