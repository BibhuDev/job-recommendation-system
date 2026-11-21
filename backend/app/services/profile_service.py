
from sqlalchemy.orm import Session
from backend.app.models.profile import UserProfile


def get_profile(db: Session, user_id: int):
    return db.query(UserProfile).filter(
        UserProfile.user_id == user_id
    ).first()


def create_profile(db: Session, user_id: int, profile_data: dict):
    profile = UserProfile(user_id=user_id, **profile_data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, profile: UserProfile, data: dict):
    for key, value in data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
