import requests
import json

def test_login_and_token():
    url = "http://localhost:8000/api/v1/auth/login"
    
    # Test login with demo credentials
    login_data = {
        "email": "demo@mywisepath.com",
        "password": "demo123"
    }
    
    print("Testing login...")
    try:
        response = requests.post(url, json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Login successful!")
            print(f"Token: {data.get('token', 'No token')[:50]}...")
            print(f"User: {data.get('username', 'No username')}")
            
            # Test roadmap generation with the token
            token = data.get('token')
            if token:
                print("\nTesting roadmap generation with token...")
                roadmap_url = "http://localhost:8000/api/v1/roadmap/generate"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                roadmap_data = {
                    "skill_level": "beginner",
                    "interests": ["AI & Machine Learning"],
                    "learning_goals": ["Kariyer Değişikliği"],
                    "available_hours_per_week": 10,
                    "target_timeline_months": 6
                }
                
                roadmap_response = requests.post(roadmap_url, json=roadmap_data, headers=headers)
                print(f"Roadmap Status: {roadmap_response.status_code}")
                
                if roadmap_response.status_code == 200:
                    print("Roadmap generation successful!")
                    roadmap_data = roadmap_response.json()
                    print(f"Roadmap Title: {roadmap_data.get('title', 'No title')}")
                    print(f"Modules: {len(roadmap_data.get('modules', []))}")
                else:
                    print(f"Roadmap Error: {roadmap_response.text}")
        else:
            print(f"Login failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login_and_token()
