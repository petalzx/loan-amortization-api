from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_by_email(db: Session, email: str) -> Optional[User]:
    # .first() or .one_or_none
    return db.query(User).filter(User.email == email).one_or_none()


def create_user(db: Session, user: UserCreate) -> User:

    existing_user = db.query(User).filter(User.email == user.email).one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email,
                   hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
