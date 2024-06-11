from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from datetime import date, time
from typing import Optional
from fastapi import HTTPException


class WaterIntakeBase(BaseModel):
    volume: float


class WaterIntakeCreate(WaterIntakeBase):
    date: date
    time: time


class WaterIntake(WaterIntakeBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True


class FoodIntakeBase(BaseModel):
    food: str
    calorie: Optional[float] = None
    image: Optional[bytes] = None


class FoodIntakeCreate(FoodIntakeBase):
    date: date
    time: time

   
class FoodIntake(FoodIntakeBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

       
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
    class Config:
        orm_mode = True


class UserSettingsShareStatus(UserId):
    is_shared_water_intake: bool = False
    is_shared_food_intake: bool = False
