from pydantic import BaseModel

from datetime import date, time


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
        
        
class UserBase(BaseModel):
    email: str
    

class UserCreate(UserBase):
    password: str
    

class User(UserBase):
    id: int
    water_intakes: list[WaterIntake] = []
    
    class Config:
        orm_mode = True
