import os
from functools import lru_cache
import app.config as conf

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@lru_cache
def get_settings():
    return conf.Settings()


if os.getenv("CONNECTION_STRING"):
    SQL_ALCHEMY_DATABASE_URL = os.getenv("CONNECTION_STRING")
else:
    SQL_ALCHEMY_DATABASE_URL = get_settings().get_url()
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_app_port():
    return int(get_settings().app_port)
