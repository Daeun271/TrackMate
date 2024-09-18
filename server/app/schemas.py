from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from datetime import datetime, date
from typing import Optional, List
from fastapi import HTTPException
from .models import TimeCategory


class WaterIntake(BaseModel):
    volume: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class WaterIntakeTotalForDateRequest(BaseModel):
    date_time: datetime


class WaterIntakeTotalForDateResponse(BaseModel):
    total_volume: float


class ActivityUid(BaseModel):
    uid: str


class FoodIntakeBase(BaseModel):
    name: str
    calories: Optional[float] = None
    consumed_at: date
    time_category: Optional[TimeCategory] = None
    
    class Config:
        from_attributes = True


class FoodIntakeCreateRequest(FoodIntakeBase):
    pass


class FoodIntakeCreateResponse(ActivityUid):
    pass


class FoodIntakeBaseWithUid(FoodIntakeBase, ActivityUid):
    pass


class DateRangeRequest(BaseModel):
    start_date: date
    end_date: date


class FoodIntakeGetResponse(FoodIntakeBaseWithUid):
    has_image: bool
    

class FoodIntakeForDateRangeResponse(BaseModel):
    foods: List[FoodIntakeGetResponse]


class FoodIntakeSearchRequest(BaseModel):
    search_date: date


class FoodIntakeUpdateRequest(FoodIntakeBaseWithUid):
    pass


class FoodIntakeDeleteRequest(ActivityUid):
    pass


class ExerciseBase(BaseModel):
    exercise_id: str
    category: str
    date: date
    duration: float
    burned_calories: Optional[float] = None
    
    class Config:
        from_attributes = True


class ExerciseBaseWithUid(ExerciseBase, ActivityUid):
    pass


class ExerciseCreateRequest(ExerciseBase):
    pass


class ExerciseCreateResponse(ActivityUid):
    pass


class ExerciseGetResponse(ExerciseBaseWithUid):
    pass


class ExerciseForDateRangeResponse(BaseModel):
    exercises: List[ExerciseGetResponse]


class ExerciseUpdateRequest(ExerciseBaseWithUid):
    pass


class ExerciseDeleteRequest(ActivityUid):
    pass


class Session(BaseModel):
    key: str    

    
class User(BaseModel):
    user_name: str
    email: EmailStr


class UserRegister(User):
    password: str
    
    @field_validator('user_name', 'email', 'password')
    def not_empty(cls, v, info: FieldValidationInfo):
        if not v or not v.strip():
            raise HTTPException(status_code=422, detail=f'empty {info.field_name}')
        
        return v
        
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(status_code=422, detail='Password must be at least 8 characters')
        
        if not any(char.isdigit() for char in v):
            raise HTTPException(status_code=422, detail='Password must have at least one numeral')
        
        if not any(char.isalpha() for char in v):
            raise HTTPException(status_code=422, detail='Password must have at least one letter')
        
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserSettingsShareStatus(BaseModel):
    is_shared_water_intake: bool = False
    is_shared_food_intake: bool = False


class UserSettingsPhoto(BaseModel):
    photo: bytes
    

class UserWeight(BaseModel):
    weight: float