
from pydantic import BaseModel, ConfigDict


class PreferenceCreate(BaseModel):
    preferred_roles: str | None = None
    preferred_locations: str | None = None
    min_salary: int | None = None
    employment_type: str | None = None
    work_mode: str | None = None


class PreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    preferred_roles: str | None
    preferred_locations: str | None
    min_salary: int | None
    employment_type: str | None
    work_mode: str | None
