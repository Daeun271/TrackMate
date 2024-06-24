from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas
import bcrypt

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserRegister):
    password_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), password_salt)
    db_user = models.User(user_name=user.user_name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    session_key = bcrypt.gensalt().hex()
    session = models.Session(key=session_key, user_id=db_user.id)
    db.add(session)
    db.commit()
    
    return schemas.Session(key=session_key)


def update_user_share_status(db: Session, user: schemas.UserSettingsShareStatus):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user is None:
        return
    db_user.is_shared_water_intake = user.is_shared_water_intake
    db_user.is_shared_food_intake = user.is_shared_food_intake
    db.commit()


def update_user_photo(db: Session, user: schemas.UserSettingsPhoto):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user is None:
        return
    db_user.photo = user.photo
    db.commit()


def get_total_water_intakes_by_user_id_and_date(db: Session, request: schemas.WaterIntakeTotalForDateRequest):
    total_volume=db.query(func.sum(models.WaterIntake.volume)).filter(models.WaterIntake.user_id == request.user_id, func.Date(models.WaterIntake.created_at) == func.Date(request.date)).scalar()
    
    if total_volume is None:
        total_volume = 0
    
    return schemas.WaterIntakeTotalForDateResponse(total_volume=total_volume)


def create_user_water_intake(db: Session, water_intake: schemas.WaterIntake):
    db_water_intake = models.WaterIntake(**water_intake.model_dump())
    db.add(db_water_intake)
    db.commit()
    db.refresh(db_water_intake)
    return db_water_intake


def get_food_intakes_by_user_id_and_date_range(db: Session, request: schemas.FoodIntakeForDateRangeRequest):
    return schemas.FoodIntakeForDateRangeResponse(
        foods=db.query(models.FoodIntake).filter(models.FoodIntake.user_id == request.user_id, func.Date(models.FoodIntake.created_at) >= func.Date(request.start_date), func.Date(models.FoodIntake.created_at) < func.Date(request.end_date)).all()
    )

def create_user_food_intake(db: Session, food_intake: schemas.FoodIntake):
    db_food_intake = models.FoodIntake(**food_intake.model_dump())
    db.add(db_food_intake)
    db.commit()
    db.refresh(db_food_intake)
    return db_food_intake