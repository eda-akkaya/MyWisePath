#!/usr/bin/env python3
"""
Test script for roadmap generation
"""

import requests
import json
import time

# Test different roadmap requests
def test_roadmap_generation():
    base_url = "http://localhost:8001"
    
    # Test cases with different interests
    test_cases = [
        {
            "name": "Python Programming",
            "interests": ["python", "programlama"],
            "skill_level": "beginner",
            "learning_goals": ["Python öğrenmek", "Web geliştirme yapmak"]
        },
        {
            "name": "Web Development",
            "interests": ["web geliştirme", "frontend", "javascript"],
            "skill_level": "intermediate",
            "learning_goals": ["Modern web uygulamaları geliştirmek", "React öğrenmek"]
        },
        {
            "name": "Data Science",
            "interests": ["veri bilimi", "data analysis", "pandas"],
            "skill_level": "beginner",
            "learning_goals": ["Veri analizi yapmak", "Makine öğrenmesi öğrenmek"]
        },
        {
            "name": "Machine Learning",
            "interests": ["makine öğrenmesi", "ai", "tensorflow"],
            "skill_level": "intermediate",
            "learning_goals": ["AI modelleri geliştirmek", "Derin öğrenme öğrenmek"]
        }
    ]
    
    print("🚀 MyWisePath Roadmap Generation Test")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   İlgi Alanları: {', '.join(test_case['interests'])}")
        print(f"   Seviye: {test_case['skill_level']}")
        print(f"   Hedefler: {', '.join(test_case['learning_goals'])}")
        
        # Create roadmap request
        roadmap_request = {
            "skill_level": test_case["skill_level"],
            "interests": test_case["interests"],
            "learning_goals": test_case["learning_goals"],
            "available_hours_per_week": 10,
            "target_timeline_months": 6
        }
        
        try:
            # Send request to roadmap generation endpoint
            response = requests.post(
                f"{base_url}/api/v1/roadmap/generate",
                json=roadmap_request,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                roadmap_data = response.json()
                print(f"   ✅ Başarılı!")
                print(f"   📖 Başlık: {roadmap_data['title']}")
                print(f"   📝 Açıklama: {roadmap_data['description']}")
                print(f"   📚 Modül Sayısı: {len(roadmap_data['modules'])}")
                print(f"   ⏱️  Toplam Süre: {roadmap_data['total_estimated_hours']} saat")
                
                # Show first module details
                if roadmap_data['modules']:
                    first_module = roadmap_data['modules'][0]
                    print(f"   🎯 İlk Modül: {first_module['title']}")
                    print(f"      Zorluk: {first_module['difficulty']}")
                    print(f"      Süre: {first_module['estimated_hours']} saat")
                
            else:
                print(f"   ❌ Hata: {response.status_code}")
                print(f"   Mesaj: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Bağlantı hatası: Backend çalışmıyor olabilir")
        except Exception as e:
            print(f"   ❌ Beklenmeyen hata: {e}")
        
        # Wait a bit between tests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🏁 Test tamamlandı!")

if __name__ == "__main__":
    test_roadmap_generation() 