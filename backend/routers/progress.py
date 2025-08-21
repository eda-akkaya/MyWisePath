from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict
from models.progress import ProgressUpdate, QuizSubmission, ProgressStatus
from services.progress_service import progress_service
from utils.auth import verify_token

router = APIRouter(prefix="/api/v1/progress", tags=["Progress"])
security = HTTPBearer()

@router.get("/roadmap/{roadmap_id}")
async def get_roadmap_progress(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Roadmap ilerlemesini getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    progress = progress_service.get_roadmap_progress(user_id, roadmap_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Roadmap ilerlemesi bulunamadı")
    
    return progress

@router.post("/roadmap/{roadmap_id}/module")
async def update_module_progress(
    roadmap_id: str,
    update: ProgressUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Modül ilerlemesini güncelle"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    # İlerleme yüzdesini kontrol et
    if update.progress_percentage < 0 or update.progress_percentage > 100:
        raise HTTPException(status_code=400, detail="İlerleme yüzdesi 0-100 arasında olmalıdır")
    
    # Zaman kontrolü
    if update.time_spent_minutes < 0:
        raise HTTPException(status_code=400, detail="Geçen süre negatif olamaz")
    
    module_progress = progress_service.update_module_progress(user_id, roadmap_id, update)
    
    return {
        "message": "Modül ilerlemesi güncellendi",
        "module_progress": module_progress
    }

@router.post("/roadmap/{roadmap_id}/quiz")
async def submit_quiz(
    roadmap_id: str,
    submission: QuizSubmission,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Quiz sonucunu gönder"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    # Quiz verilerini kontrol et
    if not submission.answers:
        raise HTTPException(status_code=400, detail="Quiz cevapları boş olamaz")
    
    if submission.time_taken_minutes < 0:
        raise HTTPException(status_code=400, detail="Geçen süre negatif olamaz")
    
    quiz_result = progress_service.submit_quiz_result(user_id, roadmap_id, submission)
    
    return {
        "message": "Quiz sonucu kaydedildi",
        "quiz_result": quiz_result,
        "passed": quiz_result.score >= 80
    }

@router.get("/summary")
async def get_user_progress_summary(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Kullanıcının genel ilerleme özetini getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    summary = progress_service.get_user_progress_summary(user_id)
    
    return summary

@router.get("/roadmap/{roadmap_id}/weekly")
async def get_weekly_progress(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Haftalık ilerleme verilerini getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    weekly_data = progress_service.get_weekly_progress(user_id, roadmap_id)
    
    return {
        "roadmap_id": roadmap_id,
        "weekly_progress": weekly_data
    }

@router.post("/roadmap/{roadmap_id}/start")
async def start_roadmap(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Roadmap'i başlat"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    # Roadmap ilerlemesi yoksa oluştur
    progress = progress_service.get_roadmap_progress(user_id, roadmap_id)
    if not progress:
        # Varsayılan modül sayısı (gerçek uygulamada roadmap'ten alınır)
        progress = progress_service.initialize_roadmap_progress(user_id, roadmap_id, 4)
    
    return {
        "message": "Roadmap başlatıldı",
        "roadmap_progress": progress
    }

@router.post("/roadmap/{roadmap_id}/module/{module_id}/complete")
async def complete_module(
    roadmap_id: str,
    module_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Modülü tamamla"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    update = ProgressUpdate(
        module_id=module_id,
        progress_percentage=100,
        time_spent_minutes=0,  # Mevcut süreyi korumak için 0 gönder
        status=ProgressStatus.COMPLETED
    )
    
    module_progress = progress_service.update_module_progress(user_id, roadmap_id, update)
    
    return {
        "message": "Modül tamamlandı",
        "module_progress": module_progress
    }

@router.get("/roadmap/{roadmap_id}/stats")
async def get_roadmap_stats(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Roadmap istatistiklerini getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    progress = progress_service.get_roadmap_progress(user_id, roadmap_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Roadmap ilerlemesi bulunamadı")
    
    # İstatistikleri hesapla
    total_quiz_attempts = 0
    average_quiz_score = 0
    total_quiz_scores = 0
    
    for module_progress in progress.module_progress:
        total_quiz_attempts += len(module_progress.quiz_results)
        for quiz_result in module_progress.quiz_results:
            total_quiz_scores += quiz_result.score
    
    if total_quiz_attempts > 0:
        average_quiz_score = total_quiz_scores / total_quiz_attempts
    
    stats = {
        "roadmap_id": roadmap_id,
        "overall_progress": progress.overall_progress,
        "completed_modules": progress.completed_modules,
        "total_modules": progress.total_modules,
        "total_time_spent_hours": round(progress.total_time_spent_minutes / 60, 1),
        "total_quiz_attempts": total_quiz_attempts,
        "average_quiz_score": round(average_quiz_score, 1),
        "estimated_completion_date": progress.estimated_completion_date,
        "started_at": progress.started_at,
        "last_activity": progress.last_activity
    }
    
    return stats
