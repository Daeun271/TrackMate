from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, LargeBinary, Enum, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum
import uuid


group_member = Table("group_members", Base.metadata, Column("user_id", Integer, ForeignKey("users.id")), Column("group_id", Integer, ForeignKey("groups.id")))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(LargeBinary, nullable=False)

    sessions = relationship("Session", back_populates="user")
    
    water_intakes = relationship("WaterIntake", back_populates="user")
    food_intakes = relationship("FoodIntake", back_populates="user")
    exercises = relationship("Exercise", back_populates="user")
    
    weight = Column(Float)
    
    groups = relationship("Group", secondary=group_member, back_populates="members")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    

class Session(Base):
    __tablename__ = "sessions"
    
    key = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="sessions")


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    
    user = relationship("User", back_populates="posts")
    group = relationship("Group", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_code = Column(String, unique=True, nullable=False, index=True)
    
    members = relationship("User", secondary=group_member, back_populates="groups")
    posts = relationship("Post", back_populates="group")
    

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
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    duration = Column(Float, nullable=False)
    burned_calories = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="exercises")
