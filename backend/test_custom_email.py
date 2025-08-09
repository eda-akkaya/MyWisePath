#!/usr/bin/env python3
"""
Test script for custom email address functionality
"""

import requests
import json

def test_custom_email():
    """Test sending email to custom address"""
    print("🧪 Testing Custom Email Address...")
    
    # Test data with custom email address
    test_data = {
        "email_type": "reminder",
        "target_email": "edaa52116@gmail.com",
        "custom_message": "Test e-postası kullanıcının girdiği adrese gönderiliyor."
    }
    
    print(f"📧 Target email: {test_data['target_email']}")
    print(f"📧 Email type: {test_data['email_type']}")
    
    # Test without authentication (should fail)
    print("\n📡 Testing without authentication...")
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
    
    print("\n✅ Custom email test completed!")
    print("Note: These tests should fail with 401/403 errors as expected")

def test_email_validation():
    """Test email validation"""
    print("\n🧪 Testing Email Validation...")
    
    invalid_emails = [
        "invalid-email",
        "test@",
        "@gmail.com",
        "",
        "test.email@",
        "test@.com"
    ]
    
    for email in invalid_emails:
        print(f"📧 Testing invalid email: '{email}'")
        try:
            if '@' not in email or email.count('@') != 1 or '.' not in email.split('@')[1]:
                print("❌ Invalid email format")
            else:
                print("✅ Valid email format")
        except:
            print("❌ Invalid email format")
    
    valid_emails = [
        "test@gmail.com",
        "user@example.com",
        "edaa52116@gmail.com"
    ]
    
    for email in valid_emails:
        print(f"📧 Testing valid email: '{email}'")
        if '@' in email and email.count('@') == 1 and '.' in email.split('@')[1]:
            print("✅ Valid email format")
        else:
            print("❌ Invalid email format")

if __name__ == "__main__":
    print("🚀 Starting Custom Email Tests...\n")
    
    try:
        test_custom_email()
        test_email_validation()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
