from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from datetime import datetime, date
from typing import Optional, List, Dict
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


class SearchRequest(BaseModel):
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
    

class UserWeight(BaseModel):
    weight: float
    

class UserStatsBase(BaseModel):
    category: Dict[str, int]
    water_intake: List[float]
    calories: List[List[float]]
    

class UserStatsResponse(BaseModel):
    weekly: UserStatsBase
    monthly: UserStatsBase


class GroupName(BaseModel):
    name: str


class GroupId(BaseModel):
    id: int


class GroupBase(GroupName, GroupId):
    code: str


class GroupsGetResponse(BaseModel):
    groups: List[GroupBase]


class PostBase(BaseModel):
    title: str
    content: str
    created_at: datetime


class PostCreateRequest(GroupId, PostBase):
    pass


class PostGetBase(PostBase):
    id: int
    user_name: str


class PostGetResponseBase(PostGetBase):
    is_user: bool = False


class PostCreateResponse(PostGetBase):
    is_user: bool = True


class PostsGetRequest(GroupId, DateRangeRequest):
    pass


class PostsSearchRequest(GroupId, SearchRequest):
    pass


class PostsGetResponse(BaseModel):
    posts: List[PostGetResponseBase]


class PostUpdateRequest(BaseModel):
    id: int
    title: str
    content: str


class PostUpdateResponse(PostCreateResponse):
    pass


class PostDeleteRequest(BaseModel):
    id: int


class GroupForInvitationReq(BaseModel):
    group_code: str


class CommentBase(BaseModel):
    content: str
    created_at: datetime
    user_name: str
    comment_id: int
    is_user: bool = False


class CommentsGetRequest(BaseModel):
    post_id: int


class CommentsGetResponse(BaseModel):
    comments: List[CommentBase]


class CommentCreateRequest(BaseModel):
    post_id: int
    content: str
    created_at: datetime
    

class CommentCreateResponse(CommentBase):
    pass


class CommentUpdateRequest(BaseModel):
    comment_id: int
    content: str


class CommentDeleteRequest(BaseModel):
    comment_id: int