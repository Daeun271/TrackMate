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
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
    "http://192.168.10.29:8000",
    "http://192.168.10.29:5173",
    "http://10.55.109.3:8000",
    "http://10.55.109.3:5173",
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


@app.get("/user/logout/current_device")
def logout_user_from_current_device(request: Request, db: Session = Depends(get_db)):
    crud.logout_user_from_current_device(db, session_key=request.headers.get('Authorization'))
    

@app.get("/user/logout/all_devices")
def logout_user_from_all_devices(request: Request, db: Session = Depends(get_db)):
    crud.logout_user_from_all_devices(db, user_id=request.state.user_id)


@app.get("/user", response_model=schemas.User)
def read_user(request: Request, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=request.state.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/user/water_intakes/create")
def create_water_intake(
    water_intake: schemas.WaterIntake, request: Request, db: Session = Depends(get_db)
):
    crud.create_water_intake(db=db, water_intake=water_intake, user_id=request.state.user_id)


@app.post("/user/water_intakes/get", response_model=schemas.WaterIntakeTotalForDateResponse)
def get_total_water_intake_by_user_id_and_date(water_intake_total_request: schemas.WaterIntakeTotalForDateRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_total_water_intakes_by_user_id_and_date(db, water_intake_total_request=water_intake_total_request, user_id=request.state.user_id)


@app.post("/user/food_intakes/create", response_model=schemas.FoodIntakeCreateResponse)
def create_food_intake(
    food_intake: schemas.FoodIntakeCreateRequest, request: Request, db: Session = Depends(get_db)
):
    return crud.create_food_intake(db=db, food_intake=food_intake, user_id=request.state.user_id)


@app.post("/user/food_intakes/get", response_model=schemas.FoodIntakeForDateRangeResponse)
def get_food_intakes_by_user_id_and_date_range(food_intakes_request: schemas.DateRangeRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_food_intakes_by_user_id_and_date_range(db, food_intakes_request=food_intakes_request, user_id=request.state.user_id)


@app.post("/user/food_intakes/search", response_model=schemas.FoodIntakeForDateRangeResponse)
def search_food_intakes(food_intakes_request: schemas.SearchRequest, request: Request, db: Session = Depends(get_db)):
    return crud.search_food_intakes(db, food_intakes_request=food_intakes_request, user_id=request.state.user_id)


@app.post("/user/food_intakes/update")
def update_food_intake(
    food_intake: schemas.FoodIntakeUpdateRequest, request: Request, db: Session = Depends(get_db)
):
    crud.update_food_intake(db=db, food_intake=food_intake, user_id=request.state.user_id)


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


@app.post("/user/exercises/create", response_model=schemas.ExerciseCreateResponse)
def create_exercise(
    exercise: schemas.ExerciseCreateRequest, request: Request, db: Session = Depends(get_db)
):
    return crud.create_exercise(db=db, exercise=exercise, user_id=request.state.user_id)


@app.post("/user/exercises/get", response_model=schemas.ExerciseForDateRangeResponse)
def get_exercises_by_user_id_and_date_range(exercises_request: schemas.DateRangeRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_exercises_by_user_id_and_date_range(db, exercises_request=exercises_request, user_id=request.state.user_id)


@app.post("/user/exercises/update")
def update_exercise(
    exercise: schemas.ExerciseUpdateRequest, request: Request, db: Session = Depends(get_db)
):
    crud.update_exercise(db=db, exercise=exercise, user_id=request.state.user_id)
    

@app.delete("/user/exercises/delete")
def delete_exercise(
    exercise: schemas.ExerciseDeleteRequest, request: Request, db: Session = Depends(get_db)
):
    crud.delete_exercise(db=db, exercise=exercise, user_id=request.state.user_id)
    

@app.post("/user/weight/upload")
def upload_user_weight(
    weight: schemas.UserWeight, request: Request, db: Session = Depends(get_db)
):
    crud.upload_user_weight(db=db, weight=weight, user_id=request.state.user_id)
    

@app.get("/user/weight/get")
def get_user_weight(request: Request, db: Session = Depends(get_db)) -> Optional[float]:
    return crud.get_user_weight(db=db, user_id=request.state.user_id)


@app.get("/user/stats/get")
def get_user_stats(request: Request, db: Session = Depends(get_db)):
    weekly_category_data = crud.get_weekly_category_data(db, user_id=request.state.user_id)
    weekly_water_intake_data = crud.get_weekly_water_intake_data(db, user_id=request.state.user_id)
    weekly_calories_data = crud.get_weekly_calories_data(db, user_id=request.state.user_id)
    monthly_category_data = crud.get_monthly_category_data(db, user_id=request.state.user_id)
    monthly_water_intake_data = crud.get_monthly_water_intake_data(db, user_id=request.state.user_id)
    monthly_calories_data = crud.get_monthly_calories_data(db, user_id=request.state.user_id)
    
    return schemas.UserStatsResponse(weekly=schemas.UserStatsBase(category=weekly_category_data, water_intake=weekly_water_intake_data, calories=weekly_calories_data), monthly=schemas.UserStatsBase(category=monthly_category_data, water_intake=monthly_water_intake_data, calories=monthly_calories_data))


@app.post("/user/groups/create", response_model=schemas.GroupBase)
def create_user_group(create_request: schemas.GroupName, request: Request, db: Session = Depends(get_db)):
    return crud.create_user_group(db, user_id=request.state.user_id, name=create_request.name)


@app.get("/user/groups/get", response_model=schemas.GroupsGetResponse)
def get_user_groups(request: Request, db: Session = Depends(get_db)):
    return crud.get_user_groups(db, user_id=request.state.user_id)


@app.post("/user/groups/members/get")
def get_group_members(get_request: schemas.GroupId, request: Request, db: Session = Depends(get_db)):
    return crud.get_group_members(db, user_id= request.state.user_id, group_id=get_request.id)


@app.post("/user/groups/posts/create", response_model=schemas.PostCreateResponse)
def create_group_post(post_create_request: schemas.PostCreateRequest, request: Request, db: Session = Depends(get_db)):
    return crud.create_group_post(db, post_create_request=post_create_request, user_id=request.state.user_id)


@app.post("/user/groups/posts/get", response_model=schemas.PostsGetResponse)
def get_group_posts(get_posts_request: schemas.PostsGetRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_group_posts_by_group_id_and_date_range(db, get_posts_request=get_posts_request, user_id=request.state.user_id)


@app.post("/user/groups/posts/search", response_model=schemas.PostsGetResponse)
def search_group_posts(search_posts_request: schemas.PostsSearchRequest, request: Request, db: Session = Depends(get_db)):
    return crud.search_group_posts(db, search_posts_request=search_posts_request, user_id=request.state.user_id)


@app.post("/user/groups/posts/update", response_model=Optional[schemas.PostUpdateResponse])
def update_group_post(post_update_request: schemas.PostUpdateRequest, db: Session = Depends(get_db)):
    return crud.update_group_post(db, post_update_request=post_update_request)


@app.delete("/user/groups/posts/delete")
def delete_group_post(post_delete_request: schemas.PostDeleteRequest, db: Session = Depends(get_db)):
    crud.delete_group_post(db, post_delete_request=post_delete_request)


@app.post("/user/groups/invite")
def add_user_to_group(invitation_req: schemas.GroupForInvitationReq, request: Request, db: Session = Depends(get_db)) -> Optional[int]:
    return crud.add_user_to_group(db, invitation_req=invitation_req, user_id=request.state.user_id)


@app.post("/user/groups/posts/comments/create")
def create_comment(comment_create_request: schemas.CommentCreateRequest, request: Request, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment_create_request=comment_create_request, user_id=request.state.user_id)


@app.post("/user/groups/posts/comments/get", response_model=schemas.CommentsGetResponse)
def get_comments(comment_get_request: schemas.CommentsGetRequest, request: Request, db: Session = Depends(get_db)):
    return crud.get_comments(db, comment_get_request=comment_get_request, user_id=request.state.user_id)


@app.post("/user/groups/posts/comments/update")
def update_comment(comment_update_request: schemas.CommentUpdateRequest, db: Session = Depends(get_db)):
    crud.update_comment(db, comment_update_request=comment_update_request)


@app.delete("/user/groups/posts/comments/delete")
def delete_comment(comment_delete_request: schemas.CommentDeleteRequest, db: Session = Depends(get_db)):
    crud.delete_comment(db, comment_delete_request=comment_delete_request)
    

@app.get("/user/name/get", response_model=schemas.UserName)
def get_user_name(request: Request, db: Session = Depends(get_db)):
    return crud.get_user_name(db, user_id=request.state.user_id)


@app.post("/user/name/update", response_model=schemas.UserName)
def update_user_name(name: schemas.UserName, request: Request, db: Session = Depends(get_db)):
    return crud.update_user_name(db, user_name=name.user_name, user_id=request.state.user_id)