from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from enum import Enum

class TimerType(str, Enum):
    POMODORO = "pomodoro"
    BREAK = "break"
    LONG_BREAK = "long_break"

class MusicGenre(str, Enum):
    AMBIENT = "ambient"
    CLASSICAL = "classical"
    LO_FI = "lo_fi"
    NATURE_SOUNDS = "nature_sounds"
    WHITE_NOISE = "white_noise"
    INSTRUMENTAL = "instrumental"
    ELECTRONIC = "electronic"

class FocusTechnique(str, Enum):
    POMODORO = "pomodoro"
    TIME_BLOCKING = "time_blocking"
    DEEP_WORK = "deep_work"
    MINDFULNESS = "mindfulness"
    PROGRESSIVE_MUSCLE_RELAXATION = "progressive_muscle_relaxation"

class TimerSession(BaseModel):
    id: str
    user_id: str
    timer_type: TimerType
    duration_minutes: int
    start_time: datetime
    end_time: Optional[datetime] = None
    completed: bool = False
    notes: Optional[str] = None

class PomodoroSettings(BaseModel):
    work_duration: int = 25  # dakika
    short_break_duration: int = 5  # dakika
    long_break_duration: int = 15  # dakika
    sessions_before_long_break: int = 4
    auto_start_breaks: bool = True
    auto_start_pomodoros: bool = False

class AmbientSound(BaseModel):
    id: str
    name: str
    genre: MusicGenre
    description: str
    duration_minutes: Optional[int] = None
    url: Optional[str] = None
    tags: List[str] = []

class FocusSession(BaseModel):
    id: str
    user_id: str
    technique: FocusTechnique
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: int
    ambient_sound: Optional[str] = None
    music_genre: Optional[MusicGenre] = None
    completed: bool = False
    effectiveness_rating: Optional[int] = None  # 1-10

class MotivationalMessage(BaseModel):
    id: str
    message: str
    category: str  # "daily", "focus", "break", "achievement"
    author: Optional[str] = None
    tags: List[str] = []

class LearningEnvironmentSettings(BaseModel):
    user_id: str
    pomodoro_settings: PomodoroSettings
    preferred_music_genres: List[MusicGenre] = []
    preferred_focus_techniques: List[FocusTechnique] = []
    reminder_enabled: bool = True
    ambient_sound_enabled: bool = True
    motivational_messages_enabled: bool = True
    auto_break_reminders: bool = True
    eye_care_reminders: bool = True

class BreakReminder(BaseModel):
    id: str
    user_id: str
    reminder_type: str  # "eye_care", "stretch", "hydration", "posture"
    message: str
    created_at: datetime
    acknowledged: bool = False
    action_taken: bool = False

class EnvironmentRecommendation(BaseModel):
    id: str
    user_id: str
    recommendation_type: str  # "lighting", "noise", "posture", "temperature"
    title: str
    description: str
    priority: str  # "low", "medium", "high"
    implemented: bool = False
    created_at: datetime 