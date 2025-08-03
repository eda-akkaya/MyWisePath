#!/usr/bin/env python3
"""
Gerçek E-posta Gönderme Testi
Bu script gerçek e-posta göndermeyi test eder.
"""

import sys
import os

# Backend klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.email_service import email_service
from services.automation_service import automation_service

def test_real_email():
    """Gerçek e-posta gönderme testi"""
    print("🧪 Gerçek E-posta Gönderme Testi")
    print("=" * 50)
    
    # SMTP bilgilerini manuel olarak ayarla
    email_service.smtp_username = "edaa52116@gmail.com"
    email_service.smtp_password = "tfkz oqmx kuiy cmow"
    email_service.smtp_server = "smtp.gmail.com"
    email_service.smtp_port = 587
    
    print("📧 E-posta ayarları kontrol ediliyor...")
    
    print(f"✅ SMTP ayarları mevcut:")
    print(f"   - Server: {email_service.smtp_server}")
    print(f"   - Port: {email_service.smtp_port}")
    print(f"   - Username: {email_service.smtp_username}")
    print(f"   - From: {email_service.email_from}")
    
    # Test kullanıcısı
    test_user = {
        "username": "Test Kullanıcı",
        "email": "edaa52116@gmail.com",  # Kendi e-posta adresinize gönder
        "learning_goals": ["Python", "JavaScript", "React"],
        "progress_data": {
            "completed_topics": ["HTML", "CSS", "JavaScript Temelleri"],
            "current_streak": 5,
            "total_study_time": 25,
            "next_goals": ["React.js", "Node.js", "Database"]
        }
    }
    
    print(f"\n📧 Test e-postası gönderiliyor: {test_user['email']}")
    
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

def test_automation_with_real_email():
    """Otomasyon servisi ile gerçek e-posta testi"""
    print("\n🤖 Otomasyon Servisi ile Gerçek E-posta Testi")
    print("=" * 50)
    
    # SMTP bilgilerini manuel olarak ayarla
    email_service.smtp_username = "edaa52116@gmail.com"
    email_service.smtp_password = "tfkz oqmx kuiy cmow"
    email_service.smtp_server = "smtp.gmail.com"
    email_service.smtp_port = 587
    
    print(f"\n📧 Test e-postası gönderiliyor: edaa52116@gmail.com")
    
    # Test e-postası gönder
    success = automation_service.send_test_email(
        email="edaa52116@gmail.com",
        email_type="reminder"
    )
    
    if success:
        print("✅ Test e-postası başarıyla gönderildi!")
        
        # İlerleme raporu da gönder
        success2 = automation_service.send_test_email(
            email="edaa52116@gmail.com",
            email_type="progress"
        )
        
        if success2:
            print("✅ İlerleme raporu da başarıyla gönderildi!")
        else:
            print("❌ İlerleme raporu gönderilemedi!")
        
        return success and success2
    else:
        print("❌ Test e-postası gönderilemedi!")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🧪 MyWisePath Gerçek E-posta Testi")
    print("=" * 60)
    
    print("✅ SMTP ayarları yapılandırıldı!")
    
    # Test seçenekleri
    print("\n📧 Test Seçenekleri:")
    print("1. E-posta Servisi Testi")
    print("2. Otomasyon Servisi Testi")
    
    choice = input("\nSeçiminizi yapın (1-2): ").strip()
    
    if choice == "1":
        test_real_email()
    elif choice == "2":
        test_automation_with_real_email()
    else:
        print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    main() 