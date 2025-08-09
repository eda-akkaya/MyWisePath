from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from services.automation_service import automation_service
from services.email_service import email_service
from models.user import EmailFrequency, UserProfileUpdate
from utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/automation", tags=["Automation"])

class TestEmailRequest(BaseModel):
    email: str
    email_type: str = "reminder"  # "reminder" veya "progress"

class UserData(BaseModel):
    id: str
    username: str
    email: str
    learning_goals: List[str] = []
    progress_data: Dict[str, Any] = {}

class AutomationStatus(BaseModel):
    is_running: bool
    scheduled_jobs: List[Dict[str, Any]]
    total_users: int

class EmailSettings(BaseModel):
    email_frequency: EmailFrequency
    weekly_reminders_enabled: bool
    progress_reports_enabled: bool
    instant_email_enabled: bool

class InstantEmailRequest(BaseModel):
    email_type: str = "reminder"  # "reminder" veya "progress"
    custom_message: Optional[str] = None
    target_email: Optional[str] = None  # Kullanıcının girdiği e-posta adresi

@router.post("/start")
async def start_automation():
    """
    E-posta otomasyonunu başlat
    """
    try:
        automation_service.start_scheduler()
        return {
            "message": "E-posta otomasyonu başlatıldı",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Otomasyon başlatılamadı: {str(e)}")

@router.post("/stop")
async def stop_automation():
    """
    E-posta otomasyonunu durdur
    """
    try:
        automation_service.stop_scheduler()
        return {
            "message": "E-posta otomasyonu durduruldu",
            "status": "stopped",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Otomasyon durdurulamadı: {str(e)}")

@router.get("/status")
async def get_automation_status():
    """
    Otomasyon durumunu getir
    """
    try:
        return AutomationStatus(
            is_running=automation_service.is_running,
            scheduled_jobs=automation_service.get_scheduled_jobs(),
            total_users=len(automation_service.sample_users)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Durum alınamadı: {str(e)}")

@router.post("/test-email")
async def send_test_email(request: TestEmailRequest):
    """
    Test e-postası gönder
    """
    try:
        success = automation_service.send_test_email(
            email=request.email,
            email_type=request.email_type
        )
        
        if success:
            return {
                "message": f"Test e-postası başarıyla gönderildi: {request.email}",
                "email_type": request.email_type,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Test e-postası gönderilemedi")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test e-postası hatası: {str(e)}")

@router.post("/send-weekly-reminders")
async def send_weekly_reminders():
    """
    Haftalık hatırlatıcıları manuel olarak gönder
    """
    try:
        automation_service.send_weekly_reminders()
        return {
            "message": "Haftalık hatırlatıcılar gönderildi",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Haftalık hatırlatıcı hatası: {str(e)}")

@router.post("/send-progress-reports")
async def send_progress_reports():
    """
    İlerleme raporlarını manuel olarak gönder
    """
    try:
        automation_service.send_progress_reports()
        return {
            "message": "İlerleme raporları gönderildi",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İlerleme raporu hatası: {str(e)}")

@router.get("/users")
async def get_users():
    """
    Otomasyon kullanıcılarını getir
    """
    try:
        return {
            "users": automation_service.sample_users,
            "total_count": len(automation_service.sample_users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcılar alınamadı: {str(e)}")

@router.post("/users")
async def add_user(user_data: UserData):
    """
    Yeni kullanıcı ekle
    """
    try:
        automation_service.add_user(user_data.dict())
        return {
            "message": f"Kullanıcı eklendi: {user_data.email}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı eklenemedi: {str(e)}")

@router.delete("/users/{email}")
async def remove_user(email: str):
    """
    Kullanıcı kaldır
    """
    try:
        automation_service.remove_user(email)
        return {
            "message": f"Kullanıcı kaldırıldı: {email}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı kaldırılamadı: {str(e)}")

@router.get("/email-settings")
async def get_email_settings(current_user: dict = Depends(get_current_user)):
    """
    Kullanıcının e-posta ayarlarını getir
    """
    try:
        # Gerçek uygulamada veritabanından alınacak
        # Şimdilik default değerler döndürüyoruz
        return EmailSettings(
            email_frequency=EmailFrequency.WEEKLY,
            weekly_reminders_enabled=True,
            progress_reports_enabled=True,
            instant_email_enabled=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"E-posta ayarları getirilemedi: {str(e)}")

@router.put("/email-settings")
async def update_email_settings(
    settings: EmailSettings,
    current_user: dict = Depends(get_current_user)
):
    """
    Kullanıcının e-posta ayarlarını güncelle
    """
    try:
        # Gerçek uygulamada veritabanına kaydedilecek
        return {
            "message": "E-posta ayarları başarıyla güncellendi",
            "settings": settings,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"E-posta ayarları güncellenemedi: {str(e)}")

@router.post("/send-instant-email")
async def send_instant_email(
    request: InstantEmailRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Anında e-posta gönder
    """
    try:
        # Kullanıcının girdiği e-posta adresini kullan, yoksa mevcut kullanıcı e-postasını kullan
        user_email = request.target_email or current_user.get("email")
        username = current_user.get("username", "Kullanıcı")
        
        if not user_email:
            raise HTTPException(status_code=400, detail="E-posta adresi bulunamadı")
        
        # E-posta adresi formatını kontrol et
        if '@' not in user_email or user_email.count('@') != 1 or '.' not in user_email.split('@')[1]:
            raise HTTPException(status_code=400, detail="Geçersiz e-posta adresi formatı")
        
        # Kullanıcının e-posta ayarlarını kontrol et
        # Gerçek uygulamada veritabanından alınacak
        instant_email_enabled = True  # Default değer
        
        if not instant_email_enabled:
            raise HTTPException(status_code=400, detail="Anında e-posta gönderimi devre dışı")
        
        success = False
        if request.email_type == "reminder":
            # Default learning goals if not available
            learning_goals = current_user.get("learning_goals", ["Öğrenme", "Gelişim"])
            if not learning_goals:
                learning_goals = ["Öğrenme", "Gelişim"]
                
            success = email_service.send_weekly_reminder(
                user_email=user_email,
                username=username,
                learning_goals=learning_goals
            )
        elif request.email_type == "progress":
            progress_data = {
                "completed_topics": ["Örnek Konu", "Temel Bilgiler"],
                "current_streak": 1,
                "total_study_time": 10,
                "next_goals": ["Hedef", "Gelişim"]
            }
            success = email_service.send_progress_report(
                user_email=user_email,
                username=username,
                progress_data=progress_data
            )
        else:
            raise HTTPException(status_code=400, detail="Geçersiz e-posta türü")
        
        if success:
            return {
                "message": f"Anında e-posta başarıyla gönderildi: {user_email}",
                "email_type": request.email_type,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="E-posta gönderilemedi")
            
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        print(f"Anında e-posta hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Anında e-posta hatası: {str(e)}")

@router.post("/schedule/custom")
async def schedule_custom_job(
    job_type: str,
    day: str,
    time: str,
    background_tasks: BackgroundTasks
):
    """
    Özel zamanlanmış iş ekle
    """
    try:
        if job_type == "weekly_reminder":
            # Özel haftalık hatırlatıcı planla
            import schedule
            schedule.every().day.at(time).do(automation_service.send_weekly_reminders)
            return {
                "message": f"Özel haftalık hatırlatıcı planlandı: {day} {time}",
                "job_type": job_type,
                "schedule": f"{day} {time}"
            }
        elif job_type == "progress_report":
            # Özel ilerleme raporu planla
            import schedule
            schedule.every().day.at(time).do(automation_service.send_progress_reports)
            return {
                "message": f"Özel ilerleme raporu planlandı: {day} {time}",
                "job_type": job_type,
                "schedule": f"{day} {time}"
            }
        else:
            raise HTTPException(status_code=400, detail="Geçersiz iş türü")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Özel iş planlanamadı: {str(e)}") 