from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EducationalContent(BaseModel):
    title: str
    platform: str
    url: str
    type: str  # course, video, interactive, book, article
    duration: str
    free: bool
    description: str
    difficulty: Optional[str] = None
    rating: Optional[float] = None
    language: Optional[str] = "Turkish"
    tags: List[str] = []

class ContentRecommendation(BaseModel):
    topic: str
    skill_level: str
    recommendations: List[EducationalContent]
    total_count: int
    timestamp: datetime

class LearningPathContent(BaseModel):
    learning_area: str
    content_list: List[EducationalContent]
    estimated_duration: str
    difficulty_progression: List[str]

class ContentSearchRequest(BaseModel):
    query: str
    skill_level: Optional[str] = "beginner"
    content_type: Optional[str] = "all"
    platform: Optional[str] = None
    free_only: Optional[bool] = False
    max_results: Optional[int] = 10

class ContentSearchResponse(BaseModel):
    query: str
    results: List[EducationalContent]
    total_count: int
    filters_applied: dict
    timestamp: datetime 