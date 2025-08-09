#!/usr/bin/env python3
"""
Test script for authenticated email sending
"""

import requests
import json

def test_authenticated_email():
    """Test sending email with authentication"""
    print("🧪 Testing Authenticated Email Sending...")
    
    # First, register a test user
    print("\n📝 Registering test user...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
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
            print(f"✅ User registered successfully")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Now test email sending with token
    print("\n📧 Testing email sending with authentication...")
    email_data = {
        "email_type": "reminder",
        "target_email": "edaa52116@gmail.com",
        "custom_message": "Test e-postası authentication ile gönderiliyor."
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/automation/send-instant-email",
            json=email_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"Email Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Email sent successfully!")
        else:
            print("❌ Email sending failed!")
            
    except Exception as e:
        print(f"❌ Email sending error: {e}")

def test_login_and_email():
    """Test login and then email sending"""
    print("\n🧪 Testing Login and Email...")
    
    # Login
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            token = user_data.get('token')
            print(f"✅ Login successful")
            print(f"Token: {token[:20]}...")
            
            # Test email sending
            email_data = {
                "email_type": "progress",
                "target_email": "edaa52116@gmail.com",
                "custom_message": "İlerleme raporu test e-postası."
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/automation/send-instant-email",
                json=email_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            print(f"Email Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Progress email sent successfully!")
            else:
                print("❌ Progress email sending failed!")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Login/Email error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Authenticated Email Tests...\n")
    
    try:
        test_authenticated_email()
        test_login_and_email()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
