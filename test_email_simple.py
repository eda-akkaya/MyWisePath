#!/usr/bin/env python3
"""
Basit E-posta Otomasyonu Test
Bu dosya e-posta servislerini doğrudan test eder.
"""

import sys
import os

# Backend klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.automation_service import automation_service
from services.email_service import email_service

def test_email_service():
    """E-posta servisini test et"""
    print("🧪 E-posta Servisi Test Ediliyor...")
    print("=" * 50)
    
    # Test kullanıcısı
    test_user = {
        "username": "Test Kullanıcı",
        "email": "edaa52116@gmail.com",
        "learning_goals": ["Python", "JavaScript", "React"],
        "progress_data": {
            "completed_topics": ["HTML", "CSS", "JavaScript Temelleri"],
            "current_streak": 5,
            "total_study_time": 25,
            "next_goals": ["React.js", "Node.js", "Database"]
        }
    }
    
    print(f"📧 Test e-postası gönderiliyor: {test_user['email']}")
    
    # Haftalık hatırlatıcı test et
    print("\n1. Haftalık Hatırlatıcı Test:")
    success1 = email_service.send_weekly_reminder(
        user_email=test_user["email"],
        username=test_user["username"],
        learning_goals=test_user["learning_goals"]
    )
    
    if success1:
        print("✅ Haftalık hatırlatıcı başarıyla gönderildi!")
    else:
        print("❌ Haftalık hatırlatıcı gönderilemedi!")
    
    # İlerleme raporu test et
    print("\n2. İlerleme Raporu Test:")
    success2 = email_service.send_progress_report(
        user_email=test_user["email"],
        username=test_user["username"],
        progress_data=test_user["progress_data"]
    )
    
    if success2:
        print("✅ İlerleme raporu başarıyla gönderildi!")
    else:
        print("❌ İlerleme raporu gönderilemedi!")
    
    return success1 and success2

def test_automation_service():
    """Otomasyon servisini test et"""
    print("\n🤖 Otomasyon Servisi Test Ediliyor...")
    print("=" * 50)
    
    # Otomasyon durumunu kontrol et
    print(f"📊 Otomasyon Durumu:")
    print(f"   - Çalışıyor: {automation_service.is_running}")
    print(f"   - Toplam Kullanıcı: {len(automation_service.sample_users)}")
    
    # Test e-postası gönder
    print(f"\n📧 Test E-postası Gönderiliyor...")
    success = automation_service.send_test_email(
        email="edaa52116@gmail.com",
        email_type="reminder"
    )
    
    if success:
        print("✅ Test e-postası başarıyla gönderildi!")
    else:
        print("❌ Test e-postası gönderilemedi!")
    
    return success

def test_automation_scheduler():
    """Otomasyon scheduler'ını test et"""
    print("\n⏰ Otomasyon Scheduler Test Ediliyor...")
    print("=" * 50)
    
    # Scheduler'ı başlat
    print("🚀 Scheduler başlatılıyor...")
    automation_service.start_scheduler()
    
    print(f"📊 Scheduler Durumu:")
    print(f"   - Çalışıyor: {automation_service.is_running}")
    
    # Planlanmış işleri listele
    jobs = automation_service.get_scheduled_jobs()
    print(f"   - Planlanmış İşler: {len(jobs)}")
    
    for i, job in enumerate(jobs, 1):
        print(f"     {i}. {job['job']}")
        print(f"        Sonraki Çalışma: {job['next_run']}")
    
    # Scheduler'ı durdur
    print("\n🛑 Scheduler durduruluyor...")
    automation_service.stop_scheduler()
    
    print(f"📊 Son Durum:")
    print(f"   - Çalışıyor: {automation_service.is_running}")
    
    return True

def main():
    """Ana test fonksiyonu"""
    print("🧪 MyWisePath E-posta Otomasyonu Basit Test")
    print("=" * 60)
    
    tests = [
        ("E-posta Servisi", test_email_service),
        ("Otomasyon Servisi", test_automation_service),
        ("Scheduler", test_automation_scheduler),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test hatası: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Sonuçları: {passed}/{total} başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı! E-posta otomasyonu çalışıyor.")
    else:
        print("⚠️  Bazı testler başarısız. Lütfen hataları kontrol edin.")
    
    print("\n📝 Notlar:")
    print("- Test modunda e-postalar gerçekten gönderilmez, sadece simüle edilir")
    print("- Gerçek e-posta göndermek için SMTP ayarlarını yapılandırın")
    print("- .env dosyasında SMTP bilgilerini tanımlayın")

if __name__ == "__main__":
    main() 