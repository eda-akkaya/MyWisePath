import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("Testing backend endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Health check: {response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test login
    try:
        login_data = {
            "email": "demo@mywisepath.com",
            "password": "demo123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Login: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get("token")
            print(f"Token received: {token[:50]}..." if token else "No token")
            
            # Test authenticated endpoints
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test email settings
            response = requests.get(f"{BASE_URL}/api/v1/automation/email-settings", headers=headers)
            print(f"Email settings: {response.status_code}")
            if response.status_code == 200:
                print(f"Email settings response: {response.json()}")
            
            # Test profile endpoint
            response = requests.get(f"{BASE_URL}/api/v1/auth/profile", headers=headers)
            print(f"Profile: {response.status_code}")
            if response.status_code == 200:
                print(f"Profile response: {response.json()}")
            
            # Test instant email
            email_data = {
                "email_type": "reminder",
                "target_email": "test@example.com"
            }
            response = requests.post(f"{BASE_URL}/api/v1/automation/send-instant-email", 
                                   json=email_data, headers=headers)
            print(f"Instant email: {response.status_code}")
            if response.status_code == 200:
                print(f"Instant email response: {response.json()}")
        else:
            print(f"Login failed: {response.text}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_endpoints()
