from pydantic import BaseModel
from datetime import date, time
from typing import Optional


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
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


class UserUpdate(User):
    is_shared_water_intake: bool = False
    is_shared_food_intake: bool = False
