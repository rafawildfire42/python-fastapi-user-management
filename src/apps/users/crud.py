from decouple import config
from sqlalchemy.orm import Session

from . import models, schemas
from .utils import get_password_hash
from src.apps.users.tasks import send_email_celery

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


send_email = config("ENABLE_SEND_EMAIL_TASK") == "1"


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, id: id):
    return db.query(models.User).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    if send_email:
        send_email_celery.delay(user.email)
        
    return db_user


def update_user(db: Session, user: schemas.UserCreate, id: int = 0, email: str = ""):

    if id:
        db_user = db.query(models.User).filter(models.User.id == id).first()
    elif email:
        db_user = db.query(models.User).filter(
            models.User.email == email).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, id: int):
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    db.delete(db_user)
    db.commit()

    response_body = {"message": f"User #{id} deleted."}

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)
