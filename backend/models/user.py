from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime
    learning_goals: Optional[List[str]] = []
    skill_level: Optional[str] = "beginner"
    interests: Optional[List[str]] = []

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str 