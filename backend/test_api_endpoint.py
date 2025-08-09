#!/usr/bin/env python3
"""
Test script for API endpoint functionality
"""

import requests
import json

def test_api_endpoint():
    """Test the API endpoint for instant email"""
    print("🧪 Testing API Endpoint...")
    
    # Test data
    test_data = {
        "email_type": "reminder",
        "custom_message": "Test message"
    }
    
    # Test without authentication (should fail)
    print("📡 Testing without authentication...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/automation/send-instant-email",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test with invalid token (should fail)
    print("\n📡 Testing with invalid token...")
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/automation/send-instant-email",
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer invalid_token"
            }
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print("\n✅ API endpoint test completed!")
    print("Note: These tests should fail with 401/403 errors as expected")

if __name__ == "__main__":
    print("🚀 Starting API Endpoint Tests...\n")
    
    try:
        test_api_endpoint()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
