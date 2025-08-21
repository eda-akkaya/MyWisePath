#!/usr/bin/env python3
"""
Test script for agents endpoint with authentication
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_agents_endpoint():
    """Test the agents roadmap creation endpoint with authentication"""
    
    print("🚀 Agents Endpoint Test Başlıyor...")
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
    
    # 2. Agents endpoint ile roadmap oluştur
    print("\n2️⃣ Agents endpoint ile roadmap oluşturuluyor...")
    
    roadmap_request = {
        "skill_level": "beginner",
        "interests": ["Python", "Web Geliştirme"],
        "learning_goals": ["Python öğrenmek", "Web uygulaması geliştirmek"],
        "available_hours_per_week": 15,
        "target_timeline_months": 6
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        roadmap_response = requests.post(
            f"{API_BASE_URL}/api/v1/agents/roadmap/create",
            json=roadmap_request,
            headers=headers
        )
        
        print(f"Response Status: {roadmap_response.status_code}")
        print(f"Response Headers: {dict(roadmap_response.headers)}")
        
        if roadmap_response.status_code == 200:
            roadmap_result = roadmap_response.json()
            print("✅ Agents endpoint ile roadmap başarıyla oluşturuldu!")
            
            # Show full response structure
            print("\n📋 Full Response Structure:")
            print(json.dumps(roadmap_result, indent=2, ensure_ascii=False))
            
            # Try to extract roadmap data
            result_data = roadmap_result.get('result', {})
            if isinstance(result_data, dict):
                # The structure is: result.result.roadmap
                nested_result = result_data.get('result', {})
                if isinstance(nested_result, dict):
                    roadmap_data = nested_result.get('roadmap', {})
                    print(f"\n📋 Başlık: {roadmap_data.get('title', 'N/A')}")
                    print(f"📝 Açıklama: {roadmap_data.get('description', 'N/A')}")
                    print(f"🗓️ Modül Sayısı: {len(roadmap_data.get('modules', []))}")
                    
                    # Modülleri göster
                    modules = roadmap_data.get('modules', [])
                    if modules:
                        print("\n   📚 Modüller:")
                        for i, module in enumerate(modules, 1):
                            print(f"      {i}. {module.get('title', 'N/A')} ({module.get('difficulty', 'N/A')})")
                            print(f"         ⏱️ {module.get('estimated_hours', 'N/A')} saat")
                else:
                    print(f"❌ Unexpected nested result structure: {type(nested_result)}")
                    print(f"   Nested Result: {nested_result}")
            else:
                print(f"❌ Unexpected result structure: {type(result_data)}")
                print(f"   Result: {result_data}")
            
        else:
            print(f"❌ Agents endpoint ile roadmap oluşturulamadı: {roadmap_response.status_code}")
            print(f"   Hata: {roadmap_response.text}")
            
    except Exception as e:
        print(f"❌ Agents endpoint roadmap oluşturma hatası: {str(e)}")
    
    print("\n" + "="*50)
    print("🎉 Test tamamlandı!")

if __name__ == "__main__":
    test_agents_endpoint()
