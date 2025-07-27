from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LearningGoal(BaseModel):
    title: str
    description: str
    target_date: Optional[str] = None

class SkillAssessment(BaseModel):
    skill_name: str
    current_level: str  # beginner, intermediate, advanced
    target_level: str
    progress_percentage: int = 0

class Module(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str  # beginner, intermediate, advanced
    estimated_hours: int
    prerequisites: List[str] = []
    resources: List[str] = []
    completed: bool = False
    progress_percentage: int = 0

class Roadmap(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    created_at: datetime
    modules: List[Module]
    learning_goals: List[LearningGoal]
    skill_assessments: List[SkillAssessment]
    total_estimated_hours: int
    completed_modules: int = 0
    overall_progress: int = 0

class RoadmapRequest(BaseModel):
    skill_level: str
    interests: List[str]
    learning_goals: List[str]
    available_hours_per_week: int
    target_timeline_months: int 