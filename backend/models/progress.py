from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"

class QuizResult(BaseModel):
    quiz_id: str
    module_id: str
    score: int  # 0-100
    total_questions: int
    correct_answers: int
    completed_at: datetime
    time_taken_minutes: int

class ModuleProgress(BaseModel):
    module_id: str
    roadmap_id: str
    user_id: str
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    progress_percentage: int = 0  # 0-100
    time_spent_minutes: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    notes: Optional[str] = None
    quiz_results: List[QuizResult] = []

class RoadmapProgress(BaseModel):
    roadmap_id: str
    user_id: str
    overall_progress: int = 0  # 0-100
    completed_modules: int = 0
    total_modules: int = 0
    total_time_spent_minutes: int = 0
    started_at: Optional[datetime] = None
    estimated_completion_date: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    module_progress: List[ModuleProgress] = []

class ProgressUpdate(BaseModel):
    module_id: str
    progress_percentage: int
    time_spent_minutes: int
    status: ProgressStatus
    notes: Optional[str] = None

class QuizSubmission(BaseModel):
    module_id: str
    quiz_id: str
    answers: Dict[str, str]  # question_id: answer
    time_taken_minutes: int
