#!/usr/bin/env python3
"""
Test script for instant email functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.email_service import email_service
from services.automation_service import automation_service

def test_email_service():
    """Test email service functionality"""
    print("🧪 Testing Email Service...")
    
    # Test email sending
    test_email = "edaa52116@gmail.com"
    test_username = "Test User"
    test_goals = ["Python", "JavaScript", "React"]
    
    print(f"📧 Sending test email to: {test_email}")
    
    # Test weekly reminder
    success = email_service.send_weekly_reminder(
        user_email=test_email,
        username=test_username,
        learning_goals=test_goals
    )
    
    if success:
        print("✅ Weekly reminder email sent successfully!")
    else:
        print("❌ Weekly reminder email failed!")
    
    # Test progress report
    progress_data = {
        "completed_topics": ["HTML", "CSS", "JavaScript"],
        "current_streak": 5,
        "total_study_time": 25,
        "next_goals": ["React.js", "Node.js", "Database"]
    }
    
    success = email_service.send_progress_report(
        user_email=test_email,
        username=test_username,
        progress_data=progress_data
    )
    
    if success:
        print("✅ Progress report email sent successfully!")
    else:
        print("❌ Progress report email failed!")

def test_automation_service():
    """Test automation service functionality"""
    print("\n🤖 Testing Automation Service...")
    
    # Test instant email
    test_email = "edaa52116@gmail.com"
    
    print(f"📧 Sending instant test email to: {test_email}")
    
    success = automation_service.send_test_email(
        email=test_email,
        email_type="reminder"
    )
    
    if success:
        print("✅ Instant test email sent successfully!")
    else:
        print("❌ Instant test email failed!")

if __name__ == "__main__":
    print("🚀 Starting Email Service Tests...\n")
    
    try:
        test_email_service()
        test_automation_service()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
