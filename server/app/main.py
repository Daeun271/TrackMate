from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import bcrypt

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/register", response_model=schemas.Session)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/user/login", response_model=schemas.Session)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    
    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email and/or password")

    session_key = bcrypt.gensalt().hex()
    session = models.Session(key=session_key, user_id=db_user.id)
    db.add(session)
    db.commit()
    return schemas.Session(key=session_key)


@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/user/settings/share_status")
def update_user_settings(user: schemas.UserSettingsShareStatus, db: Session = Depends(get_db)):
    crud.update_user_share_status(db=db, user=user)


@app.put("/user/settings/photo")
def update_user_photo(user: schemas.UserSettingsPhoto, db: Session = Depends(get_db)):
    crud.update_user_photo(db=db, user=user)


@app.post("/user/water_intakes", response_model=schemas.WaterIntake)
def create_water_intake_for_user(
    water_intake: schemas.WaterIntake, db: Session = Depends(get_db)
):
    return crud.create_user_water_intake(db=db, water_intake=water_intake)


@app.post("/user/water_intakes_total", response_model=schemas.WaterIntakeTotalForDateResponse)
def get_total_water_intake_by_user_id_and_date(request: schemas.WaterIntakeTotalForDateRequest, db: Session = Depends(get_db)):
    return crud.get_total_water_intakes_by_user_id_and_date(db, request=request)


@app.post("/user/food_intakes", response_model=schemas.FoodIntake)
def create_food_intake_for_user(
    food_intake: schemas.FoodIntake, db: Session = Depends(get_db)
):
    return crud.create_user_food_intake(db=db, food_intake=food_intake)


@app.post("/user/food_intakes_total", response_model=schemas.FoodIntakeForDateRangeResponse)
def read_food_intakes_by_user_id_and_date_range(request: schemas.FoodIntakeForDateRangeRequest, db: Session = Depends(get_db)):
    return crud.get_food_intakes_by_user_id_and_date_range(db, request=request)
