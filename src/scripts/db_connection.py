from src.database.base import SessionLocal

db_session = SessionLocal()
print(db_session.is_active)
db_session.close()
print(db_session.is_active)
