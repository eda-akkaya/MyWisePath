#!/usr/bin/env python3
"""
Test script for frontend email functionality
"""

import requests
import json

def test_frontend_email_flow():
    """Test the complete frontend email flow"""
    print("🧪 Testing Frontend Email Flow...")
    
    # 1. Register a user
    print("\n📝 Step 1: Registering user...")
    register_data = {
        "username": "frontenduser",
        "email": "frontend@test.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Register Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            token = user_data.get('token')
            print(f"✅ User registered: {user_data['email']}")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # 2. Test email settings
    print("\n📧 Step 2: Testing email settings...")
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/automation/email-settings",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"Email Settings Status: {response.status_code}")
        if response.status_code == 200:
            settings = response.json()
            print(f"✅ Email settings retrieved: {settings}")
        else:
            print(f"❌ Email settings failed: {response.text}")
    except Exception as e:
        print(f"❌ Email settings error: {e}")
    
    # 3. Test reminder email
    print("\n📧 Step 3: Testing reminder email...")
    reminder_data = {
        "email_type": "reminder",
        "target_email": "edaa52116@gmail.com",
        "custom_message": "Frontend'den hatırlatıcı e-postası test ediliyor."
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/automation/send-instant-email",
            json=reminder_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"Reminder Email Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Reminder email sent successfully!")
        else:
            print("❌ Reminder email failed!")
            
    except Exception as e:
        print(f"❌ Reminder email error: {e}")
    
    # 4. Test progress email
    print("\n📧 Step 4: Testing progress email...")
    progress_data = {
        "email_type": "progress",
        "target_email": "edaa52116@gmail.com",
        "custom_message": "Frontend'den ilerleme raporu test ediliyor."
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/automation/send-instant-email",
            json=progress_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"Progress Email Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Progress email sent successfully!")
        else:
            print("❌ Progress email failed!")
            
    except Exception as e:
        print(f"❌ Progress email error: {e}")

def test_email_validation():
    """Test email validation scenarios"""
    print("\n🧪 Testing Email Validation...")
    
    test_cases = [
        {
            "email": "valid@test.com",
            "expected": "valid"
        },
        {
            "email": "invalid-email",
            "expected": "invalid"
        },
        {
            "email": "test@",
            "expected": "invalid"
        },
        {
            "email": "@gmail.com",
            "expected": "invalid"
        },
        {
            "email": "",
            "expected": "invalid"
        }
    ]
    
    for case in test_cases:
        email = case["email"]
        expected = case["expected"]
        
        # Frontend validation logic
        is_valid = '@' in email and email.count('@') == 1 and '.' in email.split('@')[1] if '@' in email else False
        
        print(f"📧 Testing '{email}' -> Expected: {expected}, Actual: {'valid' if is_valid else 'invalid'}")
        
        if (expected == "valid" and is_valid) or (expected == "invalid" and not is_valid):
            print("✅ Validation correct")
        else:
            print("❌ Validation incorrect")

if __name__ == "__main__":
    print("🚀 Starting Frontend Email Tests...\n")
    
    try:
        test_frontend_email_flow()
        test_email_validation()
        print("\n✅ All frontend email tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
