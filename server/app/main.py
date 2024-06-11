from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/user/settings/share_status")
def update_user_settings(user: schemas.UserSettingsShareStatus, db: Session = Depends(get_db)):
    crud.update_user_share_status(db=db, user=user)


@app.post("/user/{user_id}/water_intakes", response_model=schemas.WaterIntake)
def create_water_intake_for_user(
    user_id: int, water_intake: schemas.WaterIntakeCreate, db: Session = Depends(get_db)
):
    return crud.create_user_water_intake(db=db, water_intake=water_intake, user_id=user_id)


@app.get("/user/{user_id}/water_intakes/{date}")
def get_total_water_intake_by_user_id_and_date(user_id: int, date: datetime.date, db: Session = Depends(get_db)) -> float:
    return crud.get_total_water_intakes_by_user_id_and_date(db, user_id=user_id, date=date)


@app.post("/user/{user_id}/food_intakes", response_model=schemas.FoodIntake)
def create_food_intake_for_user(
    user_id: int, food_intake: schemas.FoodIntakeCreate, db: Session = Depends(get_db)
):
    return crud.create_user_food_intake(db=db, food_intake=food_intake, user_id=user_id)


@app.get("/user/{user_id}/food_intakes/{start_date}/{end_date}", response_model=list[schemas.FoodIntake])
def read_food_intakes_by_user_id_and_date_range(user_id: int, start_date: datetime.date, end_date: datetime.date, db: Session = Depends(get_db)):
    return crud.get_food_intakes_by_user_id_and_date_range(db, user_id=user_id, start_date=start_date, end_date=end_date)
