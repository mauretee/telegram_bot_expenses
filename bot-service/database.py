import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value

POSTGRES_DB = get_env_variable("POSTGRES_DB")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
DB_HOST = get_env_variable("DB_HOST")
DB_PORT = get_env_variable("DB_PORT")

CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
engine = create_engine(CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
