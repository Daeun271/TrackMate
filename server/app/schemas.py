from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from datetime import datetime
from typing import Optional, List
from fastapi import HTTPException


class WaterIntake(BaseModel):
    volume: float
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True


class WaterIntakeTotalForDateRequest(BaseModel):
    user_id: int
    date: datetime


class WaterIntakeTotalForDateResponse(BaseModel):
    total_volume: float


class FoodIntake(BaseModel):
    food: str
    calorie: Optional[float] = None
    image: Optional[bytes] = None
    created_at: Optional[datetime] = None
    user_id: int
    
    class Config:
        from_attributes = True

   
class FoodIntakeForDateRangeRequest(BaseModel):
    user_id: int
    start_date: datetime
    end_date: datetime


class FoodIntakeForDateRangeResponse(BaseModel):
    foods: List[FoodIntake]
    
       
class UserBase(BaseModel):
    user_name: str
    email: EmailStr


class UserCreate(UserBase):
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


class UserId(BaseModel):
    id: int   

class User(UserBase, UserId):
    pass

class UserSettingsShareStatus(UserId):
    is_shared_water_intake: bool = False
    is_shared_food_intake: bool = False


class UserSettingsPhoto(UserId):
    photo: bytes