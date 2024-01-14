from src.database.base import SessionLocal

db_session = SessionLocal()
db_session.close()
