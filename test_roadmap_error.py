import requests
import json

# Test için basit bir roadmap request
def test_roadmap_generation():
    url = "http://localhost:8000/api/v1/roadmap/generate"
    
    # Test data
    test_data = {
        "skill_level": "beginner",
        "interests": ["python", "web development"],
        "learning_goals": ["programlama öğrenmek", "web sitesi yapmak"],
        "available_hours_per_week": 10,
        "target_timeline_months": 6
    }
    
    # Headers (token olmadan test)
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("Roadmap başarıyla oluşturuldu!")
            print(f"Title: {result.get('title')}")
            print(f"Modules: {len(result.get('modules', []))}")
        else:
            print("Hata oluştu!")
            
    except Exception as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    test_roadmap_generation() 