from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import bcrypt
from typing import Optional
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://192.168.10.29:8000",
    "http://192.168.10.29:5173",
]


def get_request_auth_user_id(request: Request) -> Optional[int]:
    key = request.headers.get('Authorization')  
    if key is None:
        key = request.query_params.get('auth')
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
    if request.method == "OPTIONS":
        return await call_next(request)

    whitelist = ["/user/register", "/user/login", "/docs", "/openapi.json"]
    
    if request.url.path in whitelist:
        return await call_next(request)
    
    user_id = get_request_auth_user_id(request)
    if user_id is not None:
        request.state.user_id = user_id
    else:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return await call_next(request)


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


@app.get("/user/logout_current_device")
def logout_user_from_current_device(request: Request, db: Session = Depends(get_db)):
    crud.logout_user_from_current_device(db, session_key=request.headers.get('Authorization'))
    

@app.get("/user/logout_all_devices")
def logout_user_from_all_devices(request: Request, db: Session = Depends(get_db)):
    crud.logout_user_from_all_devices(db, user_id=request.state.user_id)


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


@app.post("/user/water_intakes/create")
def create_water_intake(
    water_intake: schemas.WaterIntake, request: Request, db: Session = Depends(get_db)
):
    crud.create_water_intake(db=db, water_intake=water_intake, user_id=request.state.user_id)


@app.post("/user/water_intakes/get_total_volume", response_model=schemas.WaterIntakeTotalForDateResponse)
def get_total_water_intake_by_user_id_and_date(water_intake_total_request: schemas.WaterIntakeTotalForDateRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_total_water_intakes_by_user_id_and_date(db, water_intake_total_request=water_intake_total_request, user_id=request.state.user_id)


@app.post("/user/food_intakes/create", response_model=schemas.FoodIntakeCreateResponse)
def create_food_intake(
    food_intake: schemas.FoodIntakeCreateRequest, request: Request, db: Session = Depends(get_db)
):
    return crud.create_food_intake(db=db, food_intake=food_intake, user_id=request.state.user_id)


@app.post("/user/food_intakes/get_food_intakes", response_model=schemas.FoodIntakeForDateRangeResponse)
def get_food_intakes_by_user_id_and_date_range(food_intakes_request: schemas.FoodIntakeForDateRangeRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_food_intakes_by_user_id_and_date_range(db, food_intakes_request=food_intakes_request, user_id=request.state.user_id)


@app.post("/user/food_intakes/update", response_model=schemas.FoodIntakeUpdateResponse)
def update_food_intake(
    food_intake: schemas.FoodIntakeUpdateRequest, request: Request, db: Session = Depends(get_db)
):
    uid = crud.update_food_intake(db=db, food_intake=food_intake, user_id=request.state.user_id)
    if uid is None:
        raise HTTPException(status_code=404, detail="Food intake not found")
    return schemas.FoodIntakeUpdateResponse(uid=uid)


@app.delete("/user/food_intakes/delete")
def delete_food_intake(
    food_intake: schemas.FoodIntakeDeleteRequest, request: Request, db: Session = Depends(get_db)
):
    crud.delete_food_intake(db=db, food_intake=food_intake, user_id=request.state.user_id)


def image_path_for_uid(uid: str) -> str:
    image_base_path = os.environ.get("IMAGE_BASE_PATH")
    if image_base_path is None:
        image_base_path = os.path.join("data", "food_intake_images")
    return os.path.join(image_base_path, f"{uid}.jpeg")


@app.post("/user/food_intakes/images/{uid}")
def upload_food_image(
    uid: str, request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    db_food_intake = db.query(models.FoodIntake).filter(models.FoodIntake.uid == uid and models.FoodIntake.user_id == request.state.user_id).first()
    if db_food_intake is None:
        raise HTTPException(status_code=404, detail="Food intake not found")
    
    image = file.file.read()
    
    if len(image) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size too large")
    
    if not image.startswith(b"\xff\xd8\xff"):
        raise HTTPException(status_code=400, detail="Invalid image format")
    
    image_path = image_path_for_uid(uid)
    
    with open(image_path, "wb") as image_file:
        image_file.write(image)
        
    db_food_intake.has_image = True
    db.commit()


@app.get("/user/food_intakes/images/{uid}")
def get_food_image(uid: str, request: Request):
    image_path = image_path_for_uid(uid)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path, media_type="image/jpeg")
