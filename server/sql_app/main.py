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


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/water_intakes/", response_model=schemas.WaterIntake)
def create_water_intake_for_user(
    user_id: int, water_intake: schemas.WaterIntakeCreate, db: Session = Depends(get_db)
):
    return crud.create_user_water_intake(db=db, water_intake=water_intake, user_id=user_id)


@app.get("/users/{user_id}/water_intakes/", response_model=list[schemas.WaterIntake])
def read_water_intakes_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_water_intakes_by_user_id(db, user_id=user_id)


@app.get("/users/{user_id}/water_intakes/{date}", response_model=list[schemas.WaterIntake])
def read_water_intakes_by_user_id_and_date(user_id: int, date: datetime.date, db: Session = Depends(get_db)):
    return crud.get_water_intakes_by_user_id_and_date(db, user_id=user_id, date=date)


@app.get("/users/{user_id}/water_intakes/today", response_model=float)
def read_today_water_intakes_sum_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_today_water_intakes_sum_by_user_id(db, user_id=user_id)