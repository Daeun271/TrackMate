from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas
import bcrypt
from datetime import timedelta, datetime

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


def logout_user_from_current_device(db: Session, session_key: str):
    db.query(models.Session).filter(models.Session.key == session_key).delete()
    db.commit()


def logout_user_from_all_devices(db: Session, user_id: int):
    db.query(models.Session).filter(models.Session.user_id == user_id).delete()
    db.commit()


def update_user_share_status(db: Session, user: schemas.UserSettingsShareStatus, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return
    db_user.is_shared_water_intake = user.is_shared_water_intake
    db_user.is_shared_food_intake = user.is_shared_food_intake
    db.commit()


def update_user_photo(db: Session, user: schemas.UserSettingsPhoto, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return
    db_user.photo = user.photo
    db.commit()


def get_total_water_intakes_by_user_id_and_date(db: Session, water_intake_total_request: schemas.WaterIntakeTotalForDateRequest, user_id: int):
    total_volume = db.query(func.sum(models.WaterIntake.volume)).filter(models.WaterIntake.user_id == user_id, func.Date(models.WaterIntake.created_at) == func.Date(water_intake_total_request.date_time)).scalar()
    
    if total_volume is None:
        total_volume = 0
    
    return schemas.WaterIntakeTotalForDateResponse(total_volume=total_volume)


def create_water_intake(db: Session, water_intake: schemas.WaterIntake, user_id: int):
    db_water_intake = models.WaterIntake(**water_intake.model_dump(), user_id=user_id)
    db.add(db_water_intake)
    db.commit()
    db.refresh(db_water_intake)


def get_food_intakes_by_user_id_and_date_range(db: Session, food_intakes_request: schemas.DateRangeRequest, user_id: int):
    return schemas.FoodIntakeForDateRangeResponse(
        foods=db.query(models.FoodIntake).filter(models.FoodIntake.user_id == user_id, models.FoodIntake.consumed_at >= food_intakes_request.start_date, models.FoodIntake.consumed_at < food_intakes_request.end_date).all()
    )


def get_food_intakes(db: Session, food_intakes_request: schemas.FoodIntakeSearchRequest, user_id: int):
    dateRow = db.query(models.FoodIntake.consumed_at).filter(models.FoodIntake.user_id == user_id, models.FoodIntake.consumed_at < food_intakes_request.search_date).order_by(models.FoodIntake.consumed_at.desc()).first()
    if dateRow is None:
        return schemas.FoodIntakeForDateRangeResponse(foods=[])
    date = dateRow[0]
    today = date + timedelta(days=1)
    last_week = date - timedelta(days=7)
    return get_food_intakes_by_user_id_and_date_range(db, schemas.DateRangeRequest(start_date=last_week, end_date=today), user_id)
        

def create_food_intake(db: Session, food_intake: schemas.FoodIntakeCreateRequest, user_id: int):
    db_food_intake = models.FoodIntake(**food_intake.model_dump(), user_id=user_id)
    db.add(db_food_intake)
    db.commit()
    db.refresh(db_food_intake)
    return schemas.FoodIntakeCreateResponse(uid=db_food_intake.uid)


def update_food_intake(db: Session, food_intake: schemas.FoodIntakeUpdateRequest, user_id: int):
    db_food_intake = db.query(models.FoodIntake).filter(models.FoodIntake.user_id == user_id, models.FoodIntake.uid == food_intake.uid).first()
    if db_food_intake is None:
        return
    db_food_intake.name = food_intake.name
    db_food_intake.calories = food_intake.calories
    db_food_intake.consumed_at = food_intake.consumed_at
    db_food_intake.time_category = food_intake.time_category
    db.commit()


def delete_food_intake(db: Session, food_intake: schemas.FoodIntakeDeleteRequest, user_id: int):
    db.query(models.FoodIntake).filter(models.FoodIntake.user_id == user_id, models.FoodIntake.uid == food_intake.uid).delete()
    db.commit()
    

def get_exercises_by_user_id_and_date_range(db: Session, exercises_request: schemas.DateRangeRequest, user_id: int):
    return schemas.ExerciseForDateRangeResponse(
        exercises=db.query(models.Exercise).filter(models.Exercise.user_id == user_id, models.Exercise.date >= exercises_request.start_date, models.Exercise.date < exercises_request.end_date).all()
    )
    

def create_exercise(db: Session, exercise: schemas.ExerciseCreateRequest, user_id: int):
    db_exercise = models.Exercise(**exercise.model_dump(), user_id=user_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return schemas.ExerciseCreateResponse(uid=db_exercise.uid)


def update_exercise(db: Session, exercise: schemas.ExerciseUpdateRequest, user_id: int):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.user_id == user_id, models.Exercise.uid == exercise.uid).first()
    if db_exercise is None:
        return
    db_exercise.exercise_id = exercise.exercise_id
    db_exercise.category = exercise.category
    db_exercise.date = exercise.date
    db_exercise.duration = exercise.duration
    db_exercise.burned_calories = exercise.burned_calories
    db.commit()


def delete_exercise(db: Session, exercise: schemas.ExerciseDeleteRequest, user_id: int):
    db.query(models.Exercise).filter(models.Exercise.user_id == user_id, models.Exercise.uid == exercise.uid).delete()
    db.commit()
    

def upload_user_weight(db: Session, weight: schemas.UserWeight, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return
    db_user.weight = weight.weight
    db.commit()


def get_user_weight(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    return db_user.weight


def get_category_data(db: Session, user_id: int, count: int):
    
    category_count = {}
    
    end = datetime.now()
    start = end - timedelta(days=(count-1))
    
    exercises = db.query(models.Exercise.category, func.count(models.Exercise.category)).filter(models.Exercise.user_id == user_id, models.Exercise.date > start, models.Exercise.date <= end).group_by(models.Exercise.category).all()
    
    category_count = {}
    
    for exercise in exercises:
        category_count[exercise[0]] = exercise[1]
    
    return category_count


def get_weekly_category_data(db: Session, user_id: int):
    return get_category_data(db, user_id, 7)


def get_monthly_category_data(db: Session, user_id: int):
    return get_category_data(db, user_id, 180)


def get_water_intake_data(db: Session, user_id: int, ranges):
    water_data = []
    
    for (range_start, range_end) in ranges:
        range_sum = db.query(func.sum(models.WaterIntake.volume)).filter(models.WaterIntake.user_id == user_id, models.WaterIntake.created_at >= range_start, models.WaterIntake.created_at < range_end).scalar()
        
        if range_sum is None:
            water_data.append(0)
        else:
            water_data.append(range_sum)
            
    return water_data


def get_weekly_ranges():
    ranges = []

    now = datetime.now()
    today = datetime(now.year, now.month, now.day)

    for i in range(7):
        start = today - timedelta(days=i)
        end = today - timedelta(days=(i-1))
        ranges.insert(0, (start.date(), end.date()))
    
    return ranges


def get_monthly_ranges():
    ranges = []
    
    now = datetime.now()
    current_month = now.month
    
    for i in range(6):
        start = datetime(now.year, current_month-i, 1).date()
        end = datetime(now.year, current_month-i+1, 1).date()
        ranges.insert(0, (start, end))
    
    return ranges


def get_weekly_water_intake_data(db: Session, user_id: int):
    return get_water_intake_data(db, user_id, get_weekly_ranges())


def get_monthly_water_intake_data(db: Session, user_id: int):
    return get_water_intake_data(db, user_id, get_monthly_ranges())


def get_calories_data(db: Session, user_id: int, ranges):
    calories_data = []
    calories_burned = []
    calories_consumed = []
    
    for (range_start, range_end) in ranges:
        burned_calories = db.query(func.sum(models.Exercise.burned_calories)).filter(models.Exercise.user_id == user_id, models.Exercise.date >= range_start, models.Exercise.date < range_end).scalar()
        consumed_calories = db.query(func.sum(models.FoodIntake.calories)).filter(models.FoodIntake.user_id == user_id, models.FoodIntake.consumed_at >= range_start, models.FoodIntake.consumed_at < range_end).scalar()
        
        if burned_calories is None:
            calories_burned.append(0)
        else:
            calories_burned.append(burned_calories)
        
        if consumed_calories is None:
            calories_consumed.append(0)
        else:
            calories_consumed.append(consumed_calories)
    
    calories_data.append(calories_burned)
    calories_data.append(calories_consumed)
    
    return calories_data


def get_weekly_calories_data(db: Session, user_id: int):
    return get_calories_data(db, user_id, get_weekly_ranges())


def get_monthly_calories_data(db: Session, user_id: int):
    return get_calories_data(db, user_id, get_monthly_ranges())