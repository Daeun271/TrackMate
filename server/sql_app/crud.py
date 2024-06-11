from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas
import datetime
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(user_name=user.user_name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_share_status(db: Session, user: schemas.UserSettingsShareStatus):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user is None:
        return
    db_user.is_shared_water_intake = user.is_shared_water_intake
    db_user.is_shared_food_intake = user.is_shared_food_intake
    db.commit()


def get_total_water_intakes_by_user_id_and_date(db: Session, user_id: int, date: datetime.date):
    return db.query(func.sum(models.WaterIntake.volume)).filter(models.WaterIntake.user_id == user_id, models.WaterIntake.date == date).scalar()


def create_user_water_intake(db: Session, water_intake: schemas.WaterIntakeCreate, user_id: int):
    db_water_intake = models.WaterIntake(**water_intake.model_dump(), user_id=user_id)
    db.add(db_water_intake)
    db.commit()
    db.refresh(db_water_intake)
    return db_water_intake


def get_food_intakes_by_user_id_and_date_range(db: Session, user_id: int, start_date: datetime.date, end_date: datetime.date):
    return db.query(models.FoodIntake).filter(models.FoodIntake.user_id == user_id, models.FoodIntake.date >= start_date, models.FoodIntake.date <= end_date).all()


def create_user_food_intake(db: Session, food_intake: schemas.FoodIntakeCreate, user_id: int):
    db_food_intake = models.FoodIntake(**food_intake.model_dump(), user_id=user_id)
    db.add(db_food_intake)
    db.commit()
    db.refresh(db_food_intake)
    return db_food_intake