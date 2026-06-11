from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.engine import URL

SQLALCHEMY_DATABASE_URL = settings.database_url

is_sqlite = (
    isinstance(SQLALCHEMY_DATABASE_URL, str)
    and SQLALCHEMY_DATABASE_URL.startswith("sqlite")
) or (
    isinstance(SQLALCHEMY_DATABASE_URL, URL)
    and SQLALCHEMY_DATABASE_URL.get_backend_name() == "sqlite"
)

if is_sqlite:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

