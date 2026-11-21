
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.services.user_service import get_user_by_id
from backend.app.services.preference_service import (
    get_preferences,
    create_preferences
)
from backend.app.schemas.preference import (
    PreferenceCreate,
    PreferenceResponse
)

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.post("/{user_id}", response_model=PreferenceResponse)
def add_preferences(
    user_id: int,
    data: PreferenceCreate,
    db: Session = Depends(get_db)
):
    if not get_user_by_id(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    if get_preferences(db, user_id):
        raise HTTPException(
            status_code=409,
            detail="Preferences already exist"
        )

    return create_preferences(db, user_id, data.model_dump())


@router.get("/{user_id}", response_model=PreferenceResponse)
def read_preferences(user_id: int, db: Session = Depends(get_db)):
    preferences = get_preferences(db, user_id)

    if not preferences:
        raise HTTPException(
            status_code=404,
            detail="Preferences not found"
        )

    return preferences
