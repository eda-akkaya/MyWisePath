#!/usr/bin/env python3
"""
Roadmap oluşturma test script'i
Authentication ve roadmap generation'ı test eder
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_roadmap_creation():
    """Roadmap oluşturma işlemini test et"""
    
    print("🚀 Roadmap Oluşturma Testi Başlıyor...")
    print("="*50)
    
    # 1. Demo kullanıcı ile giriş yap
    print("1️⃣ Demo kullanıcı ile giriş yapılıyor...")
    
    login_data = {
        "email": "demo@mywisepath.com",
        "password": "demo123"
    }
    
    try:
        login_response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('token')
            print(f"✅ Giriş başarılı! Token alındı: {token[:50]}...")
        else:
            print(f"❌ Giriş başarısız: {login_response.status_code}")
            print(f"   Hata: {login_response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Backend sunucusuna bağlanılamadı!")
        print("   Backend'in çalıştığından emin olun: python main.py")
        return
    except Exception as e:
        print(f"❌ Giriş hatası: {str(e)}")
        return
    
    # 2. Roadmap oluştur
    print("\n2️⃣ Roadmap oluşturuluyor...")
    
    roadmap_request = {
        "skill_level": "beginner",
        "interests": ["Web Geliştirme", "Veri Bilimi"],
        "learning_goals": ["Kariyer Değişikliği", "Yeni Teknoloji Öğrenme"],
        "available_hours_per_week": 15,
        "target_timeline_months": 8
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        roadmap_response = requests.post(
            f"{API_BASE_URL}/api/v1/roadmap/generate",
            json=roadmap_request,
            headers=headers
        )
        
        if roadmap_response.status_code == 200:
            roadmap_result = roadmap_response.json()
            print("✅ Roadmap başarıyla oluşturuldu!")
            print(f"   📋 Başlık: {roadmap_result.get('title', 'N/A')}")
            print(f"   📝 Açıklama: {roadmap_result.get('description', 'N/A')}")
            print(f"   🗓️ Modül Sayısı: {len(roadmap_result.get('modules', []))}")
            print(f"   ⏱️ Toplam Saat: {roadmap_result.get('total_estimated_hours', 'N/A')}")
            
            # Modülleri göster
            if 'modules' in roadmap_result:
                print("\n   📚 Modüller:")
                for i, module in enumerate(roadmap_result['modules'], 1):
                    print(f"      {i}. {module.get('title', 'N/A')} ({module.get('difficulty', 'N/A')})")
                    print(f"         ⏱️ {module.get('estimated_hours', 'N/A')} saat")
            
        else:
            print(f"❌ Roadmap oluşturulamadı: {roadmap_response.status_code}")
            print(f"   Hata: {roadmap_response.text}")
            
    except Exception as e:
        print(f"❌ Roadmap oluşturma hatası: {str(e)}")
    
    print("\n" + "="*50)
    print("🎉 Test tamamlandı!")

if __name__ == "__main__":
    test_roadmap_creation()
