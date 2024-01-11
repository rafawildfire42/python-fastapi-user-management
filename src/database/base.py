from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config
import os 

db_user = config("POSTGRES_USER")
db_password = config("POSTGRES_PW")
db_database = config("POSTGRES_DB")
db_host = config("POSTGRES_HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_database}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
