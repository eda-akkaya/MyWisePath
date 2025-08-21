#!/usr/bin/env python3
"""
Backend connection test script
Tests all the endpoints that are causing issues in the frontend
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_welcome():
    """Test welcome endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/chatbot/welcome")
        print(f"✅ Welcome endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Welcome endpoint failed: {e}")
        return False

def test_public_chat():
    """Test public chat endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chatbot/query-public",
            json={"message": "Merhaba, nasılsın?"}
        )
        print(f"✅ Public chat endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Public chat endpoint failed: {e}")
        return False

def test_comprehensive_learning():
    """Test comprehensive learning endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chatbot/comprehensive-learning",
            json={"topic": "Python programming"}
        )
        print(f"✅ Comprehensive learning endpoint: {response.status_code}")
        data = response.json()
        print(f"   Topic: {data.get('topic')}")
        print(f"   SERP Results: {len(data.get('serp_results', []))}")
        print(f"   Roadmap Modules: {len(data.get('roadmap', {}).get('modules', []))}")
        return True
    except Exception as e:
        print(f"❌ Comprehensive learning endpoint failed: {e}")
        return False

def test_cors():
    """Test CORS headers"""
    try:
        response = requests.options(f"{BASE_URL}/api/v1/chatbot/welcome")
        print(f"✅ CORS test: {response.status_code}")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        print(f"   CORS Headers: {cors_headers}")
        return True
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def main():
    print("🔍 Testing Backend Connection...")
    print("=" * 50)
    
    tests = [
        test_health,
        test_welcome,
        test_public_chat,
        test_comprehensive_learning,
        test_cors,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the backend configuration.")

if __name__ == "__main__":
    main()
