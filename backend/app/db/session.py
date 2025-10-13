from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import os


# Ensure DATABASE_URL is provided via environment (.env) - for Supabase use your Postgres URL
database_url = settings.DATABASE_URL
if not database_url:
    # Fall back to a placeholder that will typically be overridden in production/dev by .env
    database_url = os.environ.get('DATABASE_URL') or "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
