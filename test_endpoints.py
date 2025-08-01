#!/usr/bin/env python3
"""
Test script for MyWisePath backend endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Error: {e}")
        return False

def test_chatbot_welcome():
    """Test chatbot welcome endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/chatbot/welcome")
        print(f"Welcome Message: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Welcome Message Error: {e}")
        return False

def test_chatbot_debug():
    """Test chatbot debug endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/chatbot/debug/test")
        print(f"Debug Test: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Debug Test Error: {e}")
        return False

def test_auth_login():
    """Test authentication login"""
    try:
        login_data = {
            "email": "demo@mywisepath.com",
            "password": "demo123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Login successful - Token: {data.get('token', 'No token')[:20]}...")
            return data.get('token')
        else:
            print(f"Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"Login Error: {e}")
        return None

def test_chatbot_query(token):
    """Test chatbot query with authentication"""
    if not token:
        print("No token available for chatbot query test")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        chat_data = {"message": "Python öğrenmek istiyorum"}
        response = requests.post(f"{BASE_URL}/api/v1/chatbot/query", json=chat_data, headers=headers)
        print(f"Chatbot Query: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Chatbot Response: {data.get('message', 'No message')[:100]}...")
            return True
        else:
            print(f"Chatbot Query failed: {response.json()}")
            return False
    except Exception as e:
        print(f"Chatbot Query Error: {e}")
        return False

def test_generate_roadmap(token):
    """Test roadmap generation with authentication"""
    if not token:
        print("No token available for roadmap generation test")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        chat_data = {"message": "Veri bilimi yol haritası oluştur"}
        response = requests.post(f"{BASE_URL}/api/v1/chatbot/generate-roadmap", json=chat_data, headers=headers)
        print(f"Generate Roadmap: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Roadmap created: {data.get('message', 'No message')}")
            print(f"Modules count: {len(data.get('roadmap', {}).get('modules', []))}")
            return True
        else:
            print(f"Generate Roadmap failed: {response.json()}")
            return False
    except Exception as e:
        print(f"Generate Roadmap Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("MyWisePath Backend Endpoint Tests")
    print("=" * 50)
    print(f"Testing at: {BASE_URL}")
    print(f"Time: {datetime.now()}")
    print()
    
    # Test basic endpoints
    health_ok = test_health()
    welcome_ok = test_chatbot_welcome()
    debug_ok = test_chatbot_debug()
    
    print()
    print("-" * 30)
    
    # Test authentication
    token = test_auth_login()
    
    print()
    print("-" * 30)
    
    # Test authenticated endpoints
    if token:
        query_ok = test_chatbot_query(token)
        roadmap_ok = test_generate_roadmap(token)
    else:
        query_ok = False
        roadmap_ok = False
    
    print()
    print("=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Welcome Message: {'✅ PASS' if welcome_ok else '❌ FAIL'}")
    print(f"Debug Test: {'✅ PASS' if debug_ok else '❌ FAIL'}")
    print(f"Authentication: {'✅ PASS' if token else '❌ FAIL'}")
    print(f"Chatbot Query: {'✅ PASS' if query_ok else '❌ FAIL'}")
    print(f"Roadmap Generation: {'✅ PASS' if roadmap_ok else '❌ FAIL'}")
    print("=" * 50)

if __name__ == "__main__":
    main() 