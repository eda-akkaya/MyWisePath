import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import random
import json

from models.learning_environment import (
    TimerSession, PomodoroSettings, AmbientSound, FocusSession,
    MotivationalMessage, LearningEnvironmentSettings, BreakReminder,
    EnvironmentRecommendation, TimerType, MusicGenre, FocusTechnique
)

class LearningEnvironmentAgent:
    def __init__(self):
        self.ambient_sounds = self._initialize_ambient_sounds()
        self.motivational_messages = self._initialize_motivational_messages()
        self.focus_techniques = self._initialize_focus_techniques()
        
    def _initialize_ambient_sounds(self) -> List[AmbientSound]:
        """Ambient ses kütüphanesini başlat"""
        return [
            AmbientSound(
                id=str(uuid.uuid4()),
                name="Yağmur Sesi",
                genre=MusicGenre.NATURE_SOUNDS,
                description="Rahatlatıcı yağmur sesi",
                duration_minutes=60,
                tags=["doğa", "yağmur", "rahatlatıcı"]
            ),
            AmbientSound(
                id=str(uuid.uuid4()),
                name="Okyanus Dalgaları",
                genre=MusicGenre.NATURE_SOUNDS,
                description="Sakin okyanus dalga sesleri",
                duration_minutes=60,
                tags=["doğa", "okyanus", "sakin"]
            ),
            AmbientSound(
                id=str(uuid.uuid4()),
                name="Kafe Ambiyansı",
                genre=MusicGenre.AMBIENT,
                description="Arka plan kafe sesleri",
                duration_minutes=45,
                tags=["kafe", "sosyal", "enerjik"]
            ),
            AmbientSound(
                id=str(uuid.uuid4()),
                name="Lo-Fi Beats",
                genre=MusicGenre.LO_FI,
                description="Rahatlatıcı lo-fi müzik",
                duration_minutes=30,
                tags=["lo-fi", "hip-hop", "chill"]
            ),
            AmbientSound(
                id=str(uuid.uuid4()),
                name="Klasik Müzik",
                genre=MusicGenre.CLASSICAL,
                description="Mozart ve Bach eserleri",
                duration_minutes=60,
                tags=["klasik", "mozart", "bach"]
            ),
            AmbientSound(
                id=str(uuid.uuid4()),
                name="Beyaz Gürültü",
                genre=MusicGenre.WHITE_NOISE,
                description="Odaklanmayı artıran beyaz gürültü",
                duration_minutes=120,
                tags=["beyaz gürültü", "odaklanma"]
            )
        ]
    
    def _initialize_motivational_messages(self) -> List[MotivationalMessage]:
        """Motivasyonel mesajları başlat"""
        return [
            MotivationalMessage(
                id=str(uuid.uuid4()),
                message="Her başarılı kişi bir zamanlar başlangıçta zorlandı. Sen de başarabilirsin! 💪",
                category="daily",
                author="Motivasyon Asistanı",
                tags=["günlük", "motivasyon"]
            ),
            MotivationalMessage(
                id=str(uuid.uuid4()),
                message="Kod yazarken her hata bir öğrenme fırsatıdır. Hatalarından ders al! 🐛",
                category="focus",
                author="Teknik Mentor",
                tags=["kodlama", "hata", "öğrenme"]
            ),
            MotivationalMessage(
                id=str(uuid.uuid4()),
                message="Mola zamanı! Gözlerini dinlendir ve bir bardak su iç. Sağlığın önemli! 👀💧",
                category="break",
                author="Sağlık Asistanı",
                tags=["mola", "sağlık", "göz bakımı"]
            ),
            MotivationalMessage(
                id=str(uuid.uuid4()),
                message="Bugün bir modülü tamamladın! Küçük adımlar büyük başarılar getirir. 🎉",
                category="achievement",
                author="Başarı Koçu",
                tags=["başarı", "ilerleme", "kutlama"]
            ),
            MotivationalMessage(
                id=str(uuid.uuid4()),
                message="Pomodoro tekniği ile odaklanmanı artır. 25 dakika odaklan, 5 dakika dinlen! ⏰",
                category="focus",
                author="Zaman Yöneticisi",
                tags=["pomodoro", "odaklanma", "zaman"]
            ),
            MotivationalMessage(
                id=str(uuid.uuid4()),
                message="Her gün biraz daha iyi ol. Mükemmel olmak zorunda değilsin, gelişmeye odaklan! 🌱",
                category="daily",
                author="Gelişim Koçu",
                tags=["gelişim", "günlük", "ilerleme"]
            )
        ]
    
    def _initialize_focus_techniques(self) -> Dict[str, Dict]:
        """Odaklanma tekniklerini başlat"""
        return {
            "pomodoro": {
                "name": "Pomodoro Tekniği",
                "description": "25 dakika odaklan, 5 dakika mola",
                "steps": [
                    "25 dakika kesintisiz çalış",
                    "5 dakika kısa mola",
                    "4 pomodoro sonrası 15 dakika uzun mola"
                ]
            },
            "deep_work": {
                "name": "Derin Çalışma",
                "description": "90 dakika kesintisiz odaklanma",
                "steps": [
                    "Telefonu sessize al",
                    "90 dakika kesintisiz çalış",
                    "30 dakika dinlen"
                ]
            },
            "mindfulness": {
                "name": "Farkındalık Tekniği",
                "description": "Nefes odaklı odaklanma",
                "steps": [
                    "Rahat bir pozisyon al",
                    "4 saniye nefes al",
                    "4 saniye nefes tut",
                    "4 saniye nefes ver"
                ]
            },
            "time_blocking": {
                "name": "Zaman Bloklama",
                "description": "Günü bloklara bölerek planlama",
                "steps": [
                    "Günü 2-3 saatlik bloklara böl",
                    "Her blokta tek bir göreve odaklan",
                    "Bloklar arası 15 dakika mola"
                ]
            }
        }
    
    def start_pomodoro_session(self, user_id: str, duration: int = 25) -> TimerSession:
        """Pomodoro oturumu başlat"""
        session = TimerSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            timer_type=TimerType.POMODORO,
            duration_minutes=duration,
            start_time=datetime.now(),
            notes="Pomodoro çalışma oturumu"
        )
        return session
    
    def start_break_session(self, user_id: str, is_long_break: bool = False) -> TimerSession:
        """Mola oturumu başlat"""
        duration = 15 if is_long_break else 5
        timer_type = TimerType.LONG_BREAK if is_long_break else TimerType.BREAK
        
        session = TimerSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            timer_type=timer_type,
            duration_minutes=duration,
            start_time=datetime.now(),
            notes=f"{'Uzun' if is_long_break else 'Kısa'} mola oturumu"
        )
        return session
    
    def get_ambient_sound_recommendation(self, user_id: str, context: str = "focus") -> AmbientSound:
        """Kullanıcıya uygun ambient ses önerisi"""
        context_recommendations = {
            "focus": [MusicGenre.WHITE_NOISE, MusicGenre.LO_FI, MusicGenre.CLASSICAL],
            "relax": [MusicGenre.NATURE_SOUNDS, MusicGenre.AMBIENT],
            "energy": [MusicGenre.ELECTRONIC, MusicGenre.INSTRUMENTAL],
            "study": [MusicGenre.CLASSICAL, MusicGenre.LO_FI, MusicGenre.WHITE_NOISE]
        }
        
        preferred_genres = context_recommendations.get(context, [MusicGenre.LO_FI])
        
        # Tercih edilen türdeki sesleri filtrele
        available_sounds = [sound for sound in self.ambient_sounds 
                          if sound.genre in preferred_genres]
        
        if not available_sounds:
            available_sounds = self.ambient_sounds
        
        return random.choice(available_sounds)
    
    def get_motivational_message(self, category: str = "daily") -> MotivationalMessage:
        """Kategoriye göre motivasyonel mesaj getir"""
        category_messages = [msg for msg in self.motivational_messages 
                           if msg.category == category]
        
        if not category_messages:
            category_messages = self.motivational_messages
        
        return random.choice(category_messages)
    
    def get_focus_technique_recommendation(self, user_id: str, session_duration: int) -> Dict:
        """Kullanıcıya uygun odaklanma tekniği önerisi"""
        if session_duration <= 30:
            technique = "pomodoro"
        elif session_duration <= 90:
            technique = "deep_work"
        else:
            technique = "time_blocking"
        
        return {
            "technique": technique,
            "details": self.focus_techniques[technique],
            "recommended_duration": session_duration
        }
    
    def create_break_reminder(self, user_id: str, reminder_type: str) -> BreakReminder:
        """Mola hatırlatıcısı oluştur"""
        reminder_messages = {
            "eye_care": "20 dakikada bir 20 saniye 20 metre uzağa bak! Gözlerini dinlendir 👀",
            "stretch": "Uzun süre oturuyorsun! Kalk ve biraz esneme yap 💪",
            "hydration": "Su içmeyi unutma! Bir bardak su iç 🥤",
            "posture": "Duruşunu kontrol et! Omuzlarını geri al ve dik otur 🧘‍♂️"
        }
        
        return BreakReminder(
            id=str(uuid.uuid4()),
            user_id=user_id,
            reminder_type=reminder_type,
            message=reminder_messages.get(reminder_type, "Mola zamanı!"),
            created_at=datetime.now()
        )
    
    def get_environment_recommendations(self, user_id: str) -> List[EnvironmentRecommendation]:
        """Öğrenme ortamı önerileri"""
        recommendations = [
            EnvironmentRecommendation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                recommendation_type="lighting",
                title="Doğal Işık Kullan",
                description="Mümkün olduğunca doğal ışık kullan. Ekran parlaklığını %70-80 arasında tut.",
                priority="medium",
                created_at=datetime.now()
            ),
            EnvironmentRecommendation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                recommendation_type="noise",
                title="Gürültü Kontrolü",
                description="Arka plan gürültüsünü azalt. Gerekirse kulaklık kullan.",
                priority="high",
                created_at=datetime.now()
            ),
            EnvironmentRecommendation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                recommendation_type="posture",
                title="Ergonomik Duruş",
                description="Ekran göz hizasında olsun. Kollar 90 derece açıda, ayaklar yerde.",
                priority="high",
                created_at=datetime.now()
            ),
            EnvironmentRecommendation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                recommendation_type="temperature",
                title="Optimal Sıcaklık",
                description="Oda sıcaklığını 20-22°C arasında tut. Havalandırmayı unutma.",
                priority="medium",
                created_at=datetime.now()
            )
        ]
        
        return recommendations
    
    def get_daily_environment_plan(self, user_id: str) -> Dict[str, Any]:
        """Günlük öğrenme ortamı planı"""
        return {
            "morning_routine": [
                "Güneş ışığında 10 dakika otur",
                "Su iç ve kahvaltı yap",
                "Çalışma alanını düzenle",
                "Günlük hedefleri belirle"
            ],
            "focus_sessions": [
                {"time": "09:00-11:00", "technique": "deep_work", "ambient": "white_noise"},
                {"time": "11:15-12:15", "technique": "pomodoro", "ambient": "lo_fi"},
                {"time": "14:00-16:00", "technique": "time_blocking", "ambient": "classical"},
                {"time": "16:15-17:15", "technique": "pomodoro", "ambient": "nature_sounds"}
            ],
            "break_reminders": [
                {"time": "10:00", "type": "eye_care"},
                {"time": "11:00", "type": "stretch"},
                {"time": "14:30", "type": "hydration"},
                {"time": "15:30", "type": "posture"}
            ],
            "evening_routine": [
                "Günlük ilerlemeyi değerlendir",
                "Yarınki planı hazırla",
                "Ekran süresini azalt",
                "Rahatlatıcı aktivite yap"
            ]
        }
    
    def analyze_user_patterns(self, user_id: str, sessions: List[TimerSession]) -> Dict[str, Any]:
        """Kullanıcı çalışma alışkanlıklarını analiz et"""
        if not sessions:
            return {"message": "Henüz yeterli veri yok"}
        
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s.completed])
        total_duration = sum(s.duration_minutes for s in sessions if s.completed)
        
        # En verimli saatleri bul
        hour_productivity = {}
        for session in sessions:
            if session.completed:
                hour = session.start_time.hour
                hour_productivity[hour] = hour_productivity.get(hour, 0) + session.duration_minutes
        
        most_productive_hour = max(hour_productivity.items(), key=lambda x: x[1])[0] if hour_productivity else 9
        
        return {
            "total_sessions": total_sessions,
            "completion_rate": (completed_sessions / total_sessions) * 100 if total_sessions > 0 else 0,
            "total_study_time": total_duration,
            "average_session_length": total_duration / completed_sessions if completed_sessions > 0 else 0,
            "most_productive_hour": most_productive_hour,
            "recommendations": self._generate_pattern_recommendations(completed_sessions, total_sessions, most_productive_hour)
        }
    
    def _generate_pattern_recommendations(self, completed: int, total: int, productive_hour: int) -> List[str]:
        """Kullanıcı alışkanlıklarına göre öneriler oluştur"""
        recommendations = []
        
        completion_rate = (completed / total) * 100 if total > 0 else 0
        
        if completion_rate < 70:
            recommendations.append("Oturumlarını daha kısa tutmayı dene (20-25 dakika)")
        
        if productive_hour < 10:
            recommendations.append("Sabah saatlerinde çok verimlisin! Önemli konuları sabah çalış")
        elif productive_hour > 16:
            recommendations.append("Akşam saatlerinde verimlisin. Günlük planını buna göre ayarla")
        
        if total < 5:
            recommendations.append("Daha sık çalışma oturumları planla")
        
        return recommendations

# Global agent instance
learning_environment_agent = LearningEnvironmentAgent() 