from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import bcrypt
from typing import Optional

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


def get_request_auth_user_id(request: Request) -> Optional[int]:
    key = request.headers.get('Authorization')  
    if key is None:
        return None

    db = SessionLocal()
    session = db.query(models.Session).filter(models.Session.key == key).first()
    db.close()

    if session is None:
        return None
    
    return session.user_id


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    whitelist = ["/user/register", "/user/login", "/docs", "/openapi.json"]
    
    if request.url.path in whitelist:
        return await call_next(request)
    
    user_id = get_request_auth_user_id(request)
    if user_id is not None:
        request.state.user_id = user_id
    else:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)


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


@app.get("/user", response_model=schemas.User)
def read_user(request: Request, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=request.state.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/user/settings/share_status")
def update_user_settings(user: schemas.UserSettingsShareStatus, request: Request, db: Session = Depends(get_db)):
    crud.update_user_share_status(db=db, user=user, user_id=request.state.user_id)


@app.put("/user/settings/photo")
def update_user_photo(user: schemas.UserSettingsPhoto, request: Request, db: Session = Depends(get_db)):
    crud.update_user_photo(db=db, user=user, user_id=request.state.user_id)


@app.post("/user/water_intakes", response_model=schemas.WaterIntake)
def create_water_intake_for_user(
    water_intake: schemas.WaterIntake, request: Request, db: Session = Depends(get_db)
):
    return crud.create_user_water_intake(db=db, water_intake=water_intake, user_id=request.state.user_id)


@app.post("/user/water_intakes_total", response_model=schemas.WaterIntakeTotalForDateResponse)
def get_total_water_intake_by_user_id_and_date(water_intake_total_request: schemas.WaterIntakeTotalForDateRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_total_water_intakes_by_user_id_and_date(db, water_intake_total_request=water_intake_total_request, user_id=request.state.user_id)


@app.post("/user/food_intakes", response_model=schemas.FoodIntake)
def create_food_intake_for_user(
    food_intake: schemas.FoodIntake, request: Request, db: Session = Depends(get_db)
):
    return crud.create_user_food_intake(db=db, food_intake=food_intake, user_id=request.state.user_id)


@app.post("/user/food_intakes_total", response_model=schemas.FoodIntakeForDateRangeResponse)
def read_food_intakes_by_user_id_and_date_range(food_intakes_request: schemas.FoodIntakeForDateRangeRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_food_intakes_by_user_id_and_date_range(db, food_intakes_request=food_intakes_request, user_id=request.state.user_id)
