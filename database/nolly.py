import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

host = os.getenv("NOLLY_HOST")
username = os.getenv("AWS_USER")
password = os.getenv("AWS_PASSWORD")
database = os.getenv("NOLLY_DB")

DB_URL = f'mysql+pymysql://{username}:{password}@{host}/{database}'

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()