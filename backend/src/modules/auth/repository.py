from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        return self._db.execute(stmt).scalar_one_or_none()

    def add_pending(self, email: str, hashed_password: str) -> User:
        user = User(email=email.lower(), hashed_password=hashed_password)
        self._db.add(user)
        return user
