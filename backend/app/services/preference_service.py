
from sqlalchemy.orm import Session
from backend.app.models.preference import UserPreference


def get_preferences(db: Session, user_id: int):
    return db.query(UserPreference).filter(
        UserPreference.user_id == user_id
    ).first()


def create_preferences(db: Session, user_id: int, data: dict):
    preferences = UserPreference(user_id=user_id, **data)
    db.add(preferences)
    db.commit()
    db.refresh(preferences)
    return preferences


def update_preferences(
    db: Session,
    preferences: UserPreference,
    data: dict
):
    for key, value in data.items():
        setattr(preferences, key, value)

    db.commit()
    db.refresh(preferences)
    return preferences
