from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    water_intakes = relationship("WaterIntake", back_populates="user")


class WaterIntake(Base):
    __tablename__ = "water_intakes"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    volume = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="water_intakes")
