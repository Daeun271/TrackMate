from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, LargeBinary, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(LargeBinary, nullable=False)
    
    is_shared_water_intake = Column(Boolean, default=False)
    is_shared_food_intake = Column(Boolean, default=False)
    
    photo = Column(LargeBinary)

    sessions = relationship("Session", back_populates="user")
    
    water_intakes = relationship("WaterIntake", back_populates="user")
    food_intakes = relationship("FoodIntake", back_populates="user")
    exercises = relationship("Exercise", back_populates="user")
    

class Session(Base):
    __tablename__ = "sessions"
    
    key = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="sessions")


class WaterIntake(Base):
    __tablename__ = "water_intakes"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    volume = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="water_intakes")


class TimeCategory(str, enum.Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    DESSERT = "DESSERT"
    NIGHT_SNACK = "NIGHT_SNACK"


class FoodIntake(Base):
    __tablename__ = "food_intakes"

    id = Column(Integer, primary_key=True)
    consumed_at = Column(Date, nullable=False)
    time_category = Column(Enum(TimeCategory))
    name = Column(String, nullable=False)
    calories = Column(Float)
    uid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    has_image = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="food_intakes")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    uid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    exercise_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    duration = Column(Float, nullable=False)
    burned_calories = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="exercises")