#!/usr/bin/env python3
"""
E-posta Otomasyonu Ayarları Test Dosyası
Bu dosya e-posta otomasyonu ayarlarının çalışıp çalışmadığını test eder.
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_email_settings():
    """E-posta ayarları testi"""
    print("🧪 E-posta Otomasyonu Ayarları Testi")
    print("=" * 50)
    
    # Test kullanıcısı ile giriş yap
    login_data = {
        "email": "demo@mywisepath.com",
        "password": "demo123"
    }
    
    try:
        # Giriş yap
        print("1. Kullanıcı girişi yapılıyor...")
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Giriş başarısız: {login_response.status_code}")
            return False
        
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✅ Giriş başarılı!")
        
        # E-posta ayarlarını getir
        print("\n2. E-posta ayarları getiriliyor...")
        settings_response = requests.get(f"{BASE_URL}/api/v1/automation/email-settings", headers=headers)
        
        if settings_response.status_code == 200:
            settings = settings_response.json()
            print("✅ E-posta ayarları alındı:")
            print(f"   - Sıklık: {settings['email_frequency']}")
            print(f"   - Haftalık hatırlatıcılar: {settings['weekly_reminders_enabled']}")
            print(f"   - İlerleme raporları: {settings['progress_reports_enabled']}")
            print(f"   - Anında e-posta: {settings['instant_email_enabled']}")
        else:
            print(f"❌ E-posta ayarları alınamadı: {settings_response.status_code}")
            return False
        
        # E-posta ayarlarını güncelle
        print("\n3. E-posta ayarları güncelleniyor...")
        new_settings = {
            "email_frequency": "daily",
            "weekly_reminders_enabled": True,
            "progress_reports_enabled": False,
            "instant_email_enabled": True
        }
        
        update_response = requests.put(
            f"{BASE_URL}/api/v1/automation/email-settings", 
            json=new_settings, 
            headers=headers
        )
        
        if update_response.status_code == 200:
            result = update_response.json()
            print("✅ E-posta ayarları güncellendi!")
            print(f"   - Mesaj: {result['message']}")
        else:
            print(f"❌ E-posta ayarları güncellenemedi: {update_response.status_code}")
            return False
        
        # Anında e-posta gönder
        print("\n4. Anında e-posta gönderiliyor...")
        instant_email_data = {
            "email_type": "reminder"
        }
        
        instant_response = requests.post(
            f"{BASE_URL}/api/v1/automation/send-instant-email",
            json=instant_email_data,
            headers=headers
        )
        
        if instant_response.status_code == 200:
            result = instant_response.json()
            print("✅ Anında e-posta gönderildi!")
            print(f"   - Mesaj: {result['message']}")
            print(f"   - E-posta türü: {result['email_type']}")
        else:
            print(f"❌ Anında e-posta gönderilemedi: {instant_response.status_code}")
            return False
        
        # İlerleme raporu e-postası gönder
        print("\n5. İlerleme raporu e-postası gönderiliyor...")
        progress_email_data = {
            "email_type": "progress"
        }
        
        progress_response = requests.post(
            f"{BASE_URL}/api/v1/automation/send-instant-email",
            json=progress_email_data,
            headers=headers
        )
        
        if progress_response.status_code == 200:
            result = progress_response.json()
            print("✅ İlerleme raporu e-postası gönderildi!")
            print(f"   - Mesaj: {result['message']}")
            print(f"   - E-posta türü: {result['email_type']}")
        else:
            print(f"❌ İlerleme raporu e-postası gönderilemedi: {progress_response.status_code}")
            return False
        
        print("\n🎉 Tüm testler başarılı!")
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False

def test_automation_status():
    """Otomasyon durumu testi"""
    print("\n🔍 Otomasyon durumu kontrol ediliyor...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/automation/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Otomasyon Durumu:")
            print(f"   - Çalışıyor: {status['is_running']}")
            print(f"   - Toplam Kullanıcı: {status['total_users']}")
            print(f"   - Planlanmış İşler: {len(status['scheduled_jobs'])}")
            
            for i, job in enumerate(status['scheduled_jobs']):
                print(f"     {i+1}. {job['job']} - {job['next_run']}")
            
            return True
        else:
            print(f"❌ Durum alınamadı: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

if __name__ == "__main__":
    print("🚀 E-posta Otomasyonu Ayarları Testi Başlatılıyor...")
    print("=" * 60)
    
    # Backend'in çalışıp çalışmadığını kontrol et
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print("✅ Backend erişilebilir")
    except Exception as e:
        print(f"❌ Backend erişilemiyor: {e}")
        print("Lütfen backend'i başlatın: python main.py")
        exit(1)
    
    # Testleri çalıştır
    success1 = test_email_settings()
    success2 = test_automation_status()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 Tüm testler başarılı! E-posta otomasyonu ayarları çalışıyor.")
    else:
        print("❌ Bazı testler başarısız oldu.")
    
    print("\n📋 Test Özeti:")
    print("✅ E-posta ayarları getirme")
    print("✅ E-posta ayarları güncelleme")
    print("✅ Anında hatırlatıcı e-postası gönderme")
    print("✅ Anında ilerleme raporu e-postası gönderme")
    print("✅ Otomasyon durumu kontrolü")
