
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Data accepted when registering a user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# Data returned by the API
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
