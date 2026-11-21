
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_data: dict):
    data = user_data.copy()
    password = data.pop("password")

    user = User(
        **data,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
