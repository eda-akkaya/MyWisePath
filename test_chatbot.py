import requests
import json

# Test URL'leri
BASE_URL = "http://localhost:8000"
CHATBOT_URL = f"{BASE_URL}/api/v1/chatbot"

def test_chatbot_endpoints():
    """Chatbot endpoint'lerini test et"""
    
    print("=== Chatbot API Test ===")
    
    # 1. Health check
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health Check Error: {e}")
    
    # 2. Debug test
    try:
        response = requests.get(f"{CHATBOT_URL}/debug/test")
        print(f"Debug Test: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Debug Test Error: {e}")
    
    # 3. Welcome message (auth gerektirmez)
    try:
        response = requests.get(f"{CHATBOT_URL}/welcome")
        print(f"Welcome Message: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Welcome Message Error: {e}")
    
    # 4. Chat query (auth gerektirir - token olmadan test)
    try:
        response = requests.post(f"{CHATBOT_URL}/query", 
                               json={"message": "Python öğrenmek istiyorum"})
        print(f"Chat Query (no auth): {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Chat Query Error: {e}")
    
    # 5. Generate roadmap (auth gerektirir - token olmadan test)
    try:
        response = requests.post(f"{CHATBOT_URL}/generate-roadmap", 
                               json={"message": "Python öğrenmek istiyorum"})
        print(f"Generate Roadmap (no auth): {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Generate Roadmap Error: {e}")

def test_ai_education_features():
    """AI destekli eğitim özelliklerini test et"""
    
    print("\n=== AI Education Features Test ===")
    
    # 1. Content recommendations (auth gerektirir)
    try:
        response = requests.get(f"{CHATBOT_URL}/content-recommendations/python")
        print(f"Content Recommendations (no auth): {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Content Recommendations Error: {e}")
    
    # 2. Education search (auth gerektirir)
    try:
        response = requests.post(f"{CHATBOT_URL}/search-education", 
                               json={"query": "machine learning", "skill_level": "beginner", "limit": 3})
        print(f"Education Search (no auth): {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Education Search Error: {e}")
    
    # 3. Popular education (auth gerektirir)
    try:
        response = requests.get(f"{CHATBOT_URL}/popular-education?limit=3")
        print(f"Popular Education (no auth): {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Popular Education Error: {e}")

if __name__ == "__main__":
    test_chatbot_endpoints()
    test_ai_education_features() 