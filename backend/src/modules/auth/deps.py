from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.modules.auth.repository import UserRepository
from src.modules.auth.service import AuthService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db, UserRepository(db))
