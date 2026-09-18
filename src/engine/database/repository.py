import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker



load_dotenv()

DATABASE_URL = os.getenv('DATABSE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL env variable is not set.")

enigne = create_engine(
    DATABASE_URL,
    pool_pre_ping = True
)

SessionLocal = sessionmaker(
    bin = engine,
    autocommit = False,
    autoflush = False,
    expire_on_commit = False
)

def get_session() -> Session:
    return SessionLocal()