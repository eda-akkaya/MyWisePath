from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EmailFrequency(str, Enum):
    NEVER = "never"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

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
    # Email automation preferences
    email_frequency: Optional[EmailFrequency] = EmailFrequency.WEEKLY
    weekly_reminders_enabled: Optional[bool] = True
    progress_reports_enabled: Optional[bool] = True
    instant_email_enabled: Optional[bool] = True

class UserProfileUpdate(BaseModel):
    skill_level: Optional[str] = None
    interests: Optional[List[str]] = None
    learning_goals: Optional[List[str]] = None
    # Email automation preferences
    email_frequency: Optional[EmailFrequency] = None
    weekly_reminders_enabled: Optional[bool] = None
    progress_reports_enabled: Optional[bool] = None
    instant_email_enabled: Optional[bool] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str 