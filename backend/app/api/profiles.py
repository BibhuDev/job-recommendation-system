
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.services.user_service import get_user_by_id
from backend.app.services.profile_service import (
    get_profile,
    create_profile
)
from backend.app.schemas.profile import ProfileCreate, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/{user_id}", response_model=ProfileResponse)
def add_profile(
    user_id: int,
    data: ProfileCreate,
    db: Session = Depends(get_db)
):
    if not get_user_by_id(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    if get_profile(db, user_id):
        raise HTTPException(status_code=409, detail="Profile already exists")

    return create_profile(db, user_id, data.model_dump())


@router.get("/{user_id}", response_model=ProfileResponse)
def read_profile(user_id: int, db: Session = Depends(get_db)):
    profile = get_profile(db, user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile
