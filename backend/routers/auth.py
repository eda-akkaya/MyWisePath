from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta
from typing import Optional, List
from pydantic import BaseModel

from models.user import UserCreate, UserLogin, UserResponse, Token, UserProfile, UserProfileUpdate, EmailFrequency
from utils.auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.constants import DUMMY_USER

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
security = HTTPBearer()

# Dummy user data (gerçek uygulamada veritabanından gelecek)
DUMMY_USERS = {
    "demo@mywisepath.com": {
        "id": "1",
        "username": "demo_user",
        "email": "demo@mywisepath.com",
        "password": "demo123",  # Gerçek uygulamada hash'lenmiş olacak
        "learning_goals": ["Veri Bilimi", "Python Programlama"],
        "skill_level": "beginner",
        "interests": ["AI", "Machine Learning", "Data Analysis"],
        # Email automation preferences
        "email_frequency": EmailFrequency.WEEKLY,
        "weekly_reminders_enabled": True,
        "progress_reports_enabled": True,
        "instant_email_enabled": True
    }
}

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Kullanıcı kaydı (dummy - her zaman başarılı)"""
    # Dummy kayıt - gerçek uygulamada veritabanına kaydedilecek
    if user.email in DUMMY_USERS:
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı")
    
    # Dummy user oluştur
    new_user = {
        "id": str(len(DUMMY_USERS) + 1),
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "learning_goals": [],
        "skill_level": "beginner",
        "interests": [],
        # Default email settings
        "email_frequency": EmailFrequency.WEEKLY,
        "weekly_reminders_enabled": True,
        "progress_reports_enabled": True,
        "instant_email_enabled": True
    }
    
    # Kullanıcıyı DUMMY_USERS'a ekle
    DUMMY_USERS[user.email] = new_user
    
    # Token oluştur
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return UserResponse(
        id=new_user["id"],
        username=new_user["username"],
        email=new_user["email"],
        created_at=DUMMY_USER["created_at"],
        token=access_token
    )

@router.post("/login", response_model=UserResponse)
async def login(user_credentials: UserLogin):
    """Kullanıcı girişi (dummy user ile)"""
    # Kullanıcıyı DUMMY_USERS'da ara
    if user_credentials.email in DUMMY_USERS:
        user = DUMMY_USERS[user_credentials.email]
        
        # Şifre kontrolü (gerçek uygulamada hash kontrolü yapılacak)
        if user["password"] == user_credentials.password:
            # Token oluştur
            access_token = create_access_token(
                data={"sub": user_credentials.email},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            return UserResponse(
                id=user["id"],
                username=user["username"],
                email=user["email"],
                created_at=DUMMY_USER["created_at"],
                token=access_token
            )
    
    raise HTTPException(status_code=401, detail="Geçersiz email veya şifre")

@router.get("/me", response_model=UserProfile)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Mevcut kullanıcı bilgilerini getir"""
    token = credentials.credentials
    from utils.auth import verify_token
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    email = payload.get("sub")
    if email not in DUMMY_USERS:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    user = DUMMY_USERS[email]
    return UserProfile(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        created_at=DUMMY_USER["created_at"],
        learning_goals=user["learning_goals"],
        skill_level=user["skill_level"],
        interests=user["interests"],
        email_frequency=user.get("email_frequency", EmailFrequency.WEEKLY),
        weekly_reminders_enabled=user.get("weekly_reminders_enabled", True),
        progress_reports_enabled=user.get("progress_reports_enabled", True),
        instant_email_enabled=user.get("instant_email_enabled", True)
    )

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Kullanıcı profil bilgilerini getir (me endpoint'i ile aynı)"""
    token = credentials.credentials
    from utils.auth import verify_token
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    email = payload.get("sub")
    if email not in DUMMY_USERS:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    user = DUMMY_USERS[email]
    return UserProfile(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        created_at=DUMMY_USER["created_at"],
        learning_goals=user["learning_goals"],
        skill_level=user["skill_level"],
        interests=user["interests"],
        email_frequency=user.get("email_frequency", EmailFrequency.WEEKLY),
        weekly_reminders_enabled=user.get("weekly_reminders_enabled", True),
        progress_reports_enabled=user.get("progress_reports_enabled", True),
        instant_email_enabled=user.get("instant_email_enabled", True)
    )

@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Kullanıcı profil bilgilerini güncelle"""
    token = credentials.credentials
    from utils.auth import verify_token
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    email = payload.get("sub")
    if email not in DUMMY_USERS:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    user = DUMMY_USERS[email]
    
    # Profil bilgilerini güncelle
    if profile_update.skill_level is not None:
        user["skill_level"] = profile_update.skill_level
    
    if profile_update.interests is not None:
        user["interests"] = profile_update.interests
    
    if profile_update.learning_goals is not None:
        user["learning_goals"] = profile_update.learning_goals
    
    # Email automation preferences
    if profile_update.email_frequency is not None:
        user["email_frequency"] = profile_update.email_frequency
    
    if profile_update.weekly_reminders_enabled is not None:
        user["weekly_reminders_enabled"] = profile_update.weekly_reminders_enabled
    
    if profile_update.progress_reports_enabled is not None:
        user["progress_reports_enabled"] = profile_update.progress_reports_enabled
    
    if profile_update.instant_email_enabled is not None:
        user["instant_email_enabled"] = profile_update.instant_email_enabled
    
    return UserProfile(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        created_at=DUMMY_USER["created_at"],
        learning_goals=user["learning_goals"],
        skill_level=user["skill_level"],
        interests=user["interests"],
        email_frequency=user.get("email_frequency", EmailFrequency.WEEKLY),
        weekly_reminders_enabled=user.get("weekly_reminders_enabled", True),
        progress_reports_enabled=user.get("progress_reports_enabled", True),
        instant_email_enabled=user.get("instant_email_enabled", True)
    ) 