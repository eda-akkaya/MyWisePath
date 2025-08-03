#!/usr/bin/env python3
"""
E-posta Otomasyonu Test Dosyası
Bu dosya e-posta otomasyonunun çalışıp çalışmadığını test eder.
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_automation_status():
    """Otomasyon durumunu test et"""
    print("🔍 Otomasyon durumu kontrol ediliyor...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/automation/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Otomasyon Durumu:")
            print(f"   - Çalışıyor: {status['is_running']}")
            print(f"   - Toplam Kullanıcı: {status['total_users']}")
            print(f"   - Planlanmış İşler: {len(status['scheduled_jobs'])}")
            return True
        else:
            print(f"❌ Durum alınamadı: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def test_start_automation():
    """Otomasyonu başlat"""
    print("\n🚀 Otomasyon başlatılıyor...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/automation/start")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            return True
        else:
            print(f"❌ Otomasyon başlatılamadı: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def test_stop_automation():
    """Otomasyonu durdur"""
    print("\n🛑 Otomasyon durduruluyor...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/automation/stop")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            return True
        else:
            print(f"❌ Otomasyon durdurulamadı: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def test_weekly_reminders():
    """Haftalık hatırlatıcıları test et"""
    print("\n📧 Haftalık hatırlatıcılar test ediliyor...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/automation/send-weekly-reminders")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            return True
        else:
            print(f"❌ Haftalık hatırlatıcılar gönderilemedi: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def test_progress_reports():
    """İlerleme raporlarını test et"""
    print("\n📊 İlerleme raporları test ediliyor...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/automation/send-progress-reports")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            return True
        else:
            print(f"❌ İlerleme raporları gönderilemedi: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def test_users():
    """Kullanıcıları test et"""
    print("\n👥 Kullanıcılar test ediliyor...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/automation/users")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Toplam {result['total_count']} kullanıcı bulundu")
            for user in result['users']:
                print(f"   - {user['username']} ({user['email']})")
            return True
        else:
            print(f"❌ Kullanıcılar alınamadı: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def test_add_user():
    """Yeni kullanıcı ekle"""
    print("\n➕ Yeni kullanıcı ekleniyor...")
    
    new_user = {
        "id": "3",
        "username": "Test Kullanıcı",
        "email": "test@example.com",
        "learning_goals": ["Test Hedef 1", "Test Hedef 2"],
        "progress_data": {
            "completed_topics": ["Test Konu 1"],
            "current_streak": 3,
            "total_study_time": 15,
            "next_goals": ["Test Hedef 3"]
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/automation/users",
            json=new_user
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            return True
        else:
            print(f"❌ Kullanıcı eklenemedi: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🧪 MyWisePath E-posta Otomasyonu Test Başlıyor...")
    print("=" * 50)
    
    # Test sırası
    tests = [
        ("Otomasyon Durumu", test_automation_status),
        ("Otomasyon Başlatma", test_start_automation),
        ("Kullanıcılar", test_users),
        ("Yeni Kullanıcı Ekleme", test_add_user),
        ("Haftalık Hatırlatıcılar", test_weekly_reminders),
        ("İlerleme Raporları", test_progress_reports),
        ("Otomasyon Durdurma", test_stop_automation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        time.sleep(1)  # API çağrıları arasında kısa bekleme
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Sonuçları: {passed}/{total} başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı! E-posta otomasyonu çalışıyor.")
    else:
        print("⚠️  Bazı testler başarısız. Lütfen hataları kontrol edin.")
    
    print("\n📝 Kullanım Notları:")
    print("- E-posta göndermek için SMTP ayarlarınızı .env dosyasında yapılandırın")
    print("- Test e-postaları için gerçek e-posta adresleri kullanın")
    print("- Otomasyonu başlatmak için: POST /api/v1/automation/start")
    print("- Durumu kontrol etmek için: GET /api/v1/automation/status")

if __name__ == "__main__":
    main() 