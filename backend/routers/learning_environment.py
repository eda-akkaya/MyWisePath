from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
import uuid

from models.learning_environment import (
    TimerSession, PomodoroSettings, AmbientSound, FocusSession,
    MotivationalMessage, LearningEnvironmentSettings, BreakReminder,
    EnvironmentRecommendation, TimerType, MusicGenre, FocusTechnique
)
from services.learning_environment_service import learning_environment_agent
from utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/learning-environment", tags=["Learning Environment"])

# Timer endpoints
@router.post("/timer/pomodoro", response_model=TimerSession)
async def start_pomodoro_session(
    duration: int = 25
):
    """Pomodoro oturumu başlat"""
    try:
        session = learning_environment_agent.start_pomodoro_session(
            user_id="anonymous",
            duration=duration
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pomodoro oturumu başlatılamadı: {str(e)}")

@router.post("/timer/break", response_model=TimerSession)
async def start_break_session(
    is_long_break: bool = False
):
    """Mola oturumu başlat"""
    try:
        session = learning_environment_agent.start_break_session(
            user_id="anonymous",
            is_long_break=is_long_break
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mola oturumu başlatılamadı: {str(e)}")

@router.put("/timer/{session_id}/complete")
async def complete_timer_session(
    session_id: str
):
    """Timer oturumunu tamamla"""
    try:
        # Burada gerçek veritabanı güncellemesi yapılacak
        return {"message": "Oturum başarıyla tamamlandı", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Oturum tamamlanamadı: {str(e)}")

# Ambient sounds endpoints
@router.get("/ambient-sounds", response_model=List[AmbientSound])
async def get_ambient_sounds():
    """Tüm ambient sesleri getir"""
    try:
        return learning_environment_agent.ambient_sounds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ambient sesler getirilemedi: {str(e)}")

@router.get("/ambient-sounds/recommendation", response_model=AmbientSound)
async def get_ambient_sound_recommendation(
    context: str = "focus"
):
    """Kullanıcıya uygun ambient ses önerisi"""
    try:
        recommendation = learning_environment_agent.get_ambient_sound_recommendation(
            user_id="anonymous",
            context=context
        )
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ambient ses önerisi alınamadı: {str(e)}")

# Motivational messages endpoints
@router.get("/motivational-messages", response_model=List[MotivationalMessage])
async def get_motivational_messages():
    """Tüm motivasyonel mesajları getir"""
    try:
        return learning_environment_agent.motivational_messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Motivasyonel mesajlar getirilemedi: {str(e)}")

@router.get("/motivational-messages/random", response_model=MotivationalMessage)
async def get_random_motivational_message(
    category: Optional[str] = "daily"
):
    """Rastgele motivasyonel mesaj getir"""
    try:
        message = learning_environment_agent.get_motivational_message(category=category)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Motivasyonel mesaj alınamadı: {str(e)}")

# Focus techniques endpoints
@router.get("/focus-techniques")
async def get_focus_techniques():
    """Tüm odaklanma tekniklerini getir"""
    try:
        return learning_environment_agent.focus_techniques
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Odaklanma teknikleri getirilemedi: {str(e)}")

@router.get("/focus-techniques/recommendation")
async def get_focus_technique_recommendation(
    session_duration: int,
    current_user: dict = Depends(get_current_user)
):
    """Kullanıcıya uygun odaklanma tekniği önerisi"""
    try:
        recommendation = learning_environment_agent.get_focus_technique_recommendation(
            user_id=current_user["id"],
            session_duration=session_duration
        )
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Odaklanma tekniği önerisi alınamadı: {str(e)}")

# Break reminders endpoints
@router.post("/break-reminders", response_model=BreakReminder)
async def create_break_reminder(
    reminder_type: str,
    current_user: dict = Depends(get_current_user)
):
    """Mola hatırlatıcısı oluştur"""
    try:
        reminder = learning_environment_agent.create_break_reminder(
            user_id=current_user["id"],
            reminder_type=reminder_type
        )
        return reminder
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mola hatırlatıcısı oluşturulamadı: {str(e)}")

# Environment recommendations endpoints
@router.get("/environment-recommendations", response_model=List[EnvironmentRecommendation])
async def get_environment_recommendations(
    current_user: dict = Depends(get_current_user)
):
    """Öğrenme ortamı önerilerini getir"""
    try:
        recommendations = learning_environment_agent.get_environment_recommendations(
            user_id=current_user["id"]
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ortam önerileri getirilemedi: {str(e)}")

# Daily plan endpoints
@router.get("/daily-plan")
async def get_daily_environment_plan(
    current_user: dict = Depends(get_current_user)
):
    """Günlük öğrenme ortamı planını getir"""
    try:
        plan = learning_environment_agent.get_daily_environment_plan(
            user_id=current_user["id"]
        )
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Günlük plan getirilemedi: {str(e)}")

# User pattern analysis endpoints
@router.get("/user-patterns")
async def analyze_user_patterns(
    current_user: dict = Depends(get_current_user)
):
    """Kullanıcı çalışma alışkanlıklarını analiz et"""
    try:
        # Burada gerçek veritabanından session verileri çekilecek
        # Şimdilik dummy data kullanıyoruz
        dummy_sessions = [
            TimerSession(
                id=str(uuid.uuid4()),
                user_id=current_user["id"],
                timer_type=TimerType.POMODORO,
                duration_minutes=25,
                start_time=datetime.now(),
                completed=True
            )
        ]
        
        analysis = learning_environment_agent.analyze_user_patterns(
            user_id=current_user["id"],
            sessions=dummy_sessions
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı analizi yapılamadı: {str(e)}")

# Settings endpoints
@router.get("/settings", response_model=LearningEnvironmentSettings)
async def get_user_settings(
    current_user: dict = Depends(get_current_user)
):
    """Kullanıcı ayarlarını getir"""
    try:
        # Burada gerçek veritabanından ayarlar çekilecek
        # Şimdilik default ayarlar döndürüyoruz
        settings = LearningEnvironmentSettings(
            user_id=current_user["id"],
            pomodoro_settings=PomodoroSettings(),
            preferred_music_genres=[MusicGenre.LO_FI, MusicGenre.CLASSICAL],
            preferred_focus_techniques=[FocusTechnique.POMODORO, FocusTechnique.DEEP_WORK],
            reminder_enabled=True,
            ambient_sound_enabled=True,
            motivational_messages_enabled=True,
            auto_break_reminders=True,
            eye_care_reminders=True
        )
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı ayarları getirilemedi: {str(e)}")

@router.put("/settings")
async def update_user_settings(
    settings: LearningEnvironmentSettings,
    current_user: dict = Depends(get_current_user)
):
    """Kullanıcı ayarlarını güncelle"""
    try:
        # Burada gerçek veritabanı güncellemesi yapılacak
        return {"message": "Ayarlar başarıyla güncellendi", "settings": settings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ayarlar güncellenemedi: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    """Öğrenme ortamı agent'ı sağlık kontrolü"""
    return {
        "status": "healthy",
        "agent": "Learning Environment Agent",
        "features": [
            "Pomodoro Timer",
            "Ambient Sounds",
            "Motivational Messages",
            "Focus Techniques",
            "Break Reminders",
            "Environment Recommendations"
        ],
        "timestamp": datetime.now().isoformat()
    } 