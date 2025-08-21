import requests
import json

# Test the roadmap generation endpoint
def test_roadmap_generation():
    url = "http://localhost:8000/api/v1/roadmap/generate"
    
    # Test data
    test_data = {
        "skill_level": "beginner",
        "interests": ["AI & Machine Learning"],
        "learning_goals": ["Kariyer Değişikliği"],
        "available_hours_per_week": 10,
        "target_timeline_months": 6
    }
    
    # Test without token first
    print("Testing without token...")
    try:
        response = requests.post(url, json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with a dummy token
    print("\nTesting with dummy token...")
    headers = {
        "Authorization": "Bearer dummy_token",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_roadmap_generation()
