import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import os
from threading import Thread

from services.email_service import email_service
from config import WEEKLY_REMINDER_ENABLED, PROGRESS_REPORT_ENABLED
from models.user import EmailFrequency

class AutomationService:
    def __init__(self):
        self.is_running = False
        self.scheduler_thread = None
        
        # Örnek kullanıcı verileri (gerçek uygulamada veritabanından gelecek)
        self.sample_users = [
            {
                "id": "1",
                "username": "Ahmet Yılmaz",
                "email": "ahmet@example.com",
                "learning_goals": ["Python Programlama", "Web Geliştirme", "Veri Analizi"],
                "progress_data": {
                    "completed_topics": ["Python Temelleri", "HTML/CSS", "JavaScript"],
                    "current_streak": 7,
                    "total_study_time": 45,
                    "next_goals": ["React.js", "Node.js", "MongoDB"]
                },
                # Email preferences
                "email_frequency": EmailFrequency.WEEKLY,
                "weekly_reminders_enabled": True,
                "progress_reports_enabled": True,
                "instant_email_enabled": True
            },
            {
                "id": "2", 
                "username": "Ayşe Demir",
                "email": "ayse@example.com",
                "learning_goals": ["Machine Learning", "Data Science", "Python"],
                "progress_data": {
                    "completed_topics": ["Python Temelleri", "Pandas", "NumPy"],
                    "current_streak": 12,
                    "total_study_time": 78,
                    "next_goals": ["Scikit-learn", "TensorFlow", "Deep Learning"]
                },
                # Email preferences
                "email_frequency": EmailFrequency.DAILY,
                "weekly_reminders_enabled": True,
                "progress_reports_enabled": False,
                "instant_email_enabled": True
            }
        ]
    
    def start_scheduler(self):
        """
        Otomasyon scheduler'ını başlat
        """
        if self.is_running:
            print("Scheduler zaten çalışıyor!")
            return
        
        self.is_running = True
        
        # Haftalık hatırlatıcıları planla (Her Pazartesi saat 09:00)
        if WEEKLY_REMINDER_ENABLED:
            schedule.every().monday.at("09:00").do(self.send_weekly_reminders)
            print("Haftalık hatırlatıcılar planlandı (Pazartesi 09:00)")
        
        # İlerleme raporlarını planla (Her Pazar saat 18:00)
        if PROGRESS_REPORT_ENABLED:
            schedule.every().sunday.at("18:00").do(self.send_progress_reports)
            print("İlerleme raporları planlandı (Pazar 18:00)")
        
        # Günlük e-postalar için (her gün saat 08:00)
        schedule.every().day.at("08:00").do(self.send_daily_emails)
        print("Günlük e-postalar planlandı (Her gün 08:00)")
        
        # Aylık e-postalar için (her ayın 1'i saat 10:00)
        schedule.every().month.at("10:00").do(self.send_monthly_emails)
        print("Aylık e-postalar planlandı (Her ayın 1'i 10:00)")
        
        # Scheduler'ı ayrı thread'de çalıştır
        self.scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        print("E-posta otomasyonu başlatıldı!")
    
    def stop_scheduler(self):
        """
        Otomasyon scheduler'ını durdur
        """
        self.is_running = False
        schedule.clear()
        print("E-posta otomasyonu durduruldu!")
    
    def _run_scheduler(self):
        """
        Scheduler'ı çalıştır
        """
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Her dakika kontrol et
    
    def send_weekly_reminders(self):
        """
        Haftalık hatırlatıcıları gönder (kullanıcı tercihlerine göre)
        """
        print(f"Haftalık hatırlatıcılar gönderiliyor... ({datetime.now()})")
        
        for user in self.sample_users:
            # Kullanıcının e-posta tercihlerini kontrol et
            if (user.get("email_frequency") == EmailFrequency.WEEKLY and 
                user.get("weekly_reminders_enabled", True)):
                try:
                    success = email_service.send_weekly_reminder(
                        user_email=user["email"],
                        username=user["username"],
                        learning_goals=user["learning_goals"]
                    )
                    
                    if success:
                        print(f"Haftalık hatırlatıcı gönderildi: {user['email']}")
                    else:
                        print(f"Haftalık hatırlatıcı gönderilemedi: {user['email']}")
                        
                except Exception as e:
                    print(f"Haftalık hatırlatıcı hatası ({user['email']}): {e}")
    
    def send_progress_reports(self):
        """
        İlerleme raporlarını gönder (kullanıcı tercihlerine göre)
        """
        print(f"İlerleme raporları gönderiliyor... ({datetime.now()})")
        
        for user in self.sample_users:
            # Kullanıcının e-posta tercihlerini kontrol et
            if (user.get("email_frequency") == EmailFrequency.WEEKLY and 
                user.get("progress_reports_enabled", True)):
                try:
                    success = email_service.send_progress_report(
                        user_email=user["email"],
                        username=user["username"],
                        progress_data=user["progress_data"]
                    )
                    
                    if success:
                        print(f"İlerleme raporu gönderildi: {user['email']}")
                    else:
                        print(f"İlerleme raporu gönderilemedi: {user['email']}")
                        
                except Exception as e:
                    print(f"İlerleme raporu hatası ({user['email']}): {e}")
    
    def send_daily_emails(self):
        """
        Günlük e-postaları gönder
        """
        print(f"Günlük e-postalar gönderiliyor... ({datetime.now()})")
        
        for user in self.sample_users:
            if user.get("email_frequency") == EmailFrequency.DAILY:
                try:
                    # Günlük hatırlatıcı gönder
                    if user.get("weekly_reminders_enabled", True):
                        success = email_service.send_weekly_reminder(
                            user_email=user["email"],
                            username=user["username"],
                            learning_goals=user["learning_goals"]
                        )
                        
                        if success:
                            print(f"Günlük hatırlatıcı gönderildi: {user['email']}")
                        else:
                            print(f"Günlük hatırlatıcı gönderilemedi: {user['email']}")
                            
                except Exception as e:
                    print(f"Günlük e-posta hatası ({user['email']}): {e}")
    
    def send_monthly_emails(self):
        """
        Aylık e-postaları gönder
        """
        print(f"Aylık e-postalar gönderiliyor... ({datetime.now()})")
        
        for user in self.sample_users:
            if user.get("email_frequency") == EmailFrequency.MONTHLY:
                try:
                    # Aylık ilerleme raporu gönder
                    if user.get("progress_reports_enabled", True):
                        success = email_service.send_progress_report(
                            user_email=user["email"],
                            username=user["username"],
                            progress_data=user["progress_data"]
                        )
                        
                        if success:
                            print(f"Aylık ilerleme raporu gönderildi: {user['email']}")
                        else:
                            print(f"Aylık ilerleme raporu gönderilemedi: {user['email']}")
                            
                except Exception as e:
                    print(f"Aylık e-posta hatası ({user['email']}): {e}")
    
    def send_test_email(self, email: str, email_type: str = "reminder"):
        """
        Test e-postası gönder
        """
        test_user = {
            "username": "Test Kullanıcı",
            "email": email,
            "learning_goals": ["Python", "JavaScript", "React"],
            "progress_data": {
                "completed_topics": ["HTML", "CSS", "JavaScript Temelleri"],
                "current_streak": 5,
                "total_study_time": 25,
                "next_goals": ["React.js", "Node.js", "Database"]
            }
        }
        
        try:
            print(f"📧 Test e-postası gönderiliyor: {email} ({email_type})")
            
            if email_type == "reminder":
                success = email_service.send_weekly_reminder(
                    user_email=test_user["email"],
                    username=test_user["username"],
                    learning_goals=test_user["learning_goals"]
                )
            elif email_type == "progress":
                success = email_service.send_progress_report(
                    user_email=test_user["email"],
                    username=test_user["username"],
                    progress_data=test_user["progress_data"]
                )
            else:
                print(f"❌ Geçersiz e-posta türü: {email_type}")
                return False
            
            if success:
                print(f"✅ Test e-postası başarıyla gönderildi: {email}")
                return True
            else:
                print(f"❌ Test e-postası gönderilemedi: {email}")
                return False
                
        except Exception as e:
            print(f"❌ Test e-postası hatası: {e}")
            return False
    
    def get_scheduled_jobs(self) -> List[Dict[str, Any]]:
        """
        Planlanmış işleri getir
        """
        jobs = []
        for job in schedule.jobs:
            jobs.append({
                "job": str(job.job_func),
                "next_run": job.next_run.isoformat() if job.next_run else None,
                "interval": str(job.interval),
                "unit": job.unit
            })
        return jobs
    
    def add_user(self, user_data: Dict[str, Any]):
        """
        Yeni kullanıcı ekle
        """
        self.sample_users.append(user_data)
        print(f"Yeni kullanıcı eklendi: {user_data['email']}")
    
    def remove_user(self, email: str):
        """
        Kullanıcı kaldır
        """
        self.sample_users = [user for user in self.sample_users if user["email"] != email]
        print(f"Kullanıcı kaldırıldı: {email}")

# Global automation service instance
automation_service = AutomationService() 