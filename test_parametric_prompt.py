#!/usr/bin/env python3
"""
Test script for roadmap-based parametric system prompt functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.ai_service import AIService

def test_roadmap_based_prompt():
    """Test the roadmap-based system prompt with different user scenarios"""
    
    ai_service = AIService()
    
    # Test cases with different roadmap scenarios
    test_cases = [
        {
            "name": "Beginner Python Developer - Part Time",
            "roadmap_info": {
                "skill_level": "beginner",
                "interests": ["Python", "Web Development"],
                "learning_goals": ["Python Programming", "Web Development"],
                "available_hours_per_week": 5,
                "target_timeline_months": 6
            },
            "message": "Python öğrenmek istiyorum"
        },
        {
            "name": "Intermediate AI Developer - Full Time",
            "roadmap_info": {
                "skill_level": "intermediate",
                "interests": ["AI", "Machine Learning", "Data Science"],
                "learning_goals": ["Deep Learning", "TensorFlow"],
                "available_hours_per_week": 25,
                "target_timeline_months": 3
            },
            "message": "Machine learning projeleri yapmak istiyorum"
        },
        {
            "name": "Advanced Web Developer - Intensive",
            "roadmap_info": {
                "skill_level": "advanced",
                "interests": ["React", "Node.js", "Full Stack"],
                "learning_goals": ["Microservices", "Cloud Architecture"],
                "available_hours_per_week": 40,
                "target_timeline_months": 12
            },
            "message": "Microservices mimarisi hakkında bilgi ver"
        },
        {
            "name": "No Roadmap Info (Default)",
            "roadmap_info": None,
            "message": "Programlama öğrenmek istiyorum"
        }
    ]
    
    print("🧪 Testing Roadmap-Based Parametric System Prompt\n")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print("-" * 50)
        
        # Generate dynamic system prompt
        if test_case['roadmap_info']:
            system_prompt = ai_service._generate_roadmap_based_system_prompt(test_case['roadmap_info'])
        else:
            system_prompt = ai_service._generate_dynamic_system_prompt(None)
        
        print(f"👤 Roadmap Info: {test_case['roadmap_info']}")
        print(f"💬 User Message: {test_case['message']}")
        print(f"\n🤖 Generated System Prompt:")
        print("-" * 40)
        print(system_prompt)
        print("-" * 40)
        
        # Test AI response (if API key is available)
        try:
            response = ai_service.get_ai_response(
                test_case['message'], 
                roadmap_info=test_case['roadmap_info']
            )
            print(f"\n✅ AI Response:")
            print(response)
        except Exception as e:
            print(f"\n❌ AI Response Error: {e}")
        
        print("\n" + "=" * 70)

def test_time_based_instructions():
    """Test time-based instructions"""
    
    ai_service = AIService()
    
    time_scenarios = [
        {"hours": 3, "months": 3, "name": "Very Limited Time"},
        {"hours": 10, "months": 6, "name": "Moderate Time"},
        {"hours": 25, "months": 12, "name": "Intensive Learning"},
        {"hours": 40, "months": 24, "name": "Full Time Study"}
    ]
    
    print("\n⏰ Testing Time-Based Instructions\n")
    print("=" * 50)
    
    for scenario in time_scenarios:
        instructions = ai_service._get_time_based_instructions(scenario["hours"], scenario["months"])
        print(f"\n📊 Scenario: {scenario['name']}")
        print(f"Hours per week: {scenario['hours']}, Timeline: {scenario['months']} months")
        print("-" * 30)
        print(instructions)

def test_level_specific_instructions():
    """Test level-specific instructions"""
    
    ai_service = AIService()
    
    levels = ["beginner", "intermediate", "advanced"]
    
    print("\n🎯 Testing Level-Specific Instructions\n")
    print("=" * 50)
    
    for level in levels:
        instructions = ai_service._get_level_specific_instructions(level)
        print(f"\n📊 Level: {level.upper()}")
        print("-" * 20)
        print(instructions)

def test_interest_specific_instructions():
    """Test interest-specific instructions"""
    
    ai_service = AIService()
    
    interest_groups = [
        ["AI", "Machine Learning"],
        ["Web Development", "JavaScript", "React"],
        ["Python", "Data Science"],
        ["Mobile Development", "iOS", "Android"]
    ]
    
    print("\n🎨 Testing Interest-Specific Instructions\n")
    print("=" * 50)
    
    for interests in interest_groups:
        instructions = ai_service._get_interest_specific_instructions(interests)
        print(f"\n🎯 Interests: {interests}")
        print("-" * 30)
        print(instructions if instructions else "No specific instructions")

if __name__ == "__main__":
    print("🚀 Starting Roadmap-Based Parametric System Prompt Tests")
    
    # Test level-specific instructions
    test_level_specific_instructions()
    
    # Test interest-specific instructions
    test_interest_specific_instructions()
    
    # Test time-based instructions
    test_time_based_instructions()
    
    # Test full roadmap-based prompt
    test_roadmap_based_prompt()
    
    print("\n✅ All tests completed!") 