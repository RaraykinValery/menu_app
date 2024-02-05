from fastapi import Depends
from sqlalchemy.orm import Session

from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repository(repository):
    def _get_repository(session: Session = Depends(get_db)):
        return repository(session)

    return _get_repository
