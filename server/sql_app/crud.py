from sqlalchemy.orm import Session

from . import models, schemas

import datetime
from sqlalchemy.sql import func


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_water_intakes_by_user_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first().water_intakes


def get_water_intakes_by_user_id_and_date(db: Session, user_id: int, date: datetime.date):
    return db.query(models.WaterIntake).filter(models.WaterIntake.user_id == user_id, models.WaterIntake.date == date).all()


def get_today_water_intakes_sum_by_user_id(db: Session, user_id: int):
    return db.query(func.sum(models.WaterIntake.volume)).filter(models.WaterIntake.user_id == user_id, models.WaterIntake.date == datetime.date.today()).scalar()


def create_user_water_intake(db: Session, water_intake: schemas.WaterIntakeCreate, user_id: int):
    db_water_intake = models.WaterIntake(**water_intake.model_dump(), user_id=user_id)
    db.add(db_water_intake)
    db.commit()
    db.refresh(db_water_intake)
    return db_water_intake
