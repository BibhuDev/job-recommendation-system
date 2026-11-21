
from pydantic import BaseModel, ConfigDict


# Data accepted when creating or updating a profile
class ProfileCreate(BaseModel):
    headline: str | None = None
    location: str | None = None
    experience_years: int = 0
    skills: str | None = None
    education: str | None = None
    bio: str | None = None


# Data returned by the API
class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    headline: str | None
    location: str | None
    experience_years: int
    skills: str | None
    education: str | None
    bio: str | None
