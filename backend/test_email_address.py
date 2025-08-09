#!/usr/bin/env python3
"""
Simple test to verify email address is updated
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.automation_service import automation_service

def test_email_address():
    """Test that the email address is updated correctly"""
    print("🧪 Testing Email Address Update...")
    
    # Test the automation service sample users
    print("📧 Sample users email addresses:")
    for user in automation_service.sample_users:
        print(f"   - {user['username']}: {user['email']}")
    
    # Test the send_test_email function
    print("\n📧 Testing send_test_email function:")
    test_email = "edaa52116@gmail.com"
    print(f"   Using email: {test_email}")
    
    success = automation_service.send_test_email(
        email=test_email,
        email_type="reminder"
    )
    
    if success:
        print("✅ Test email sent successfully!")
    else:
        print("❌ Test email failed!")

if __name__ == "__main__":
    print("🚀 Starting Email Address Test...\n")
    
    try:
        test_email_address()
        print("\n✅ Email address test completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
