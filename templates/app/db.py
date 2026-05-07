
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings


def _ensure_db_dir():
    if settings.DB_URL.startswith('sqlite:///'):
        path = settings.DB_URL.replace('sqlite:///', '')
        if path and path != ':memory:':
            d = os.path.dirname(path)
            if d:
                os.makedirs(d, exist_ok=True)


_ensure_db_dir()
engine = create_engine(settings.DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


class Base(DeclarativeBase):
    pass
