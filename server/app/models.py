from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Float, LargeBinary
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    
    is_shared_water_intake = Column(Boolean, default=False)
    is_shared_food_intake = Column(Boolean, default=False)

    water_intakes = relationship("WaterIntake", back_populates="user")
    food_intakes = relationship("FoodIntake", back_populates="user")


class WaterIntake(Base):
    __tablename__ = "water_intakes"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    volume = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="water_intakes")


class FoodIntake(Base):
    __tablename__ = "food_intakes"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    food = Column(String, nullable=False)
    calorie = Column(Float)
    image = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="food_intakes")