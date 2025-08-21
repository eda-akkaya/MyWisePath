#!/usr/bin/env python3
"""
LangChain Agent Test Script
Test the new LangChain-based agent implementation
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.langchain_agent import langchain_roadmap_agent
from agents.agent_manager import agent_manager

def print_separator(title):
    """Print a separator with title"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

async def test_langchain_agent():
    """Test LangChain agent functionality"""
    
    print_separator("LANGCHAIN AGENT TEST")
    print_info("Testing LangChain-based roadmap generation agent")
    
    # Test 1: Agent Status
    print_separator("1. AGENT STATUS TEST")
    try:
        status = langchain_roadmap_agent.get_status()
        print_info(f"Agent Name: {status['name']}")
        print_info(f"Description: {status['description']}")
        print_info(f"Framework: {status['framework']}")
        print_info(f"Is Active: {status['is_active']}")
        print_info(f"Tools Count: {status['tools_count']}")
        print_success("Agent status retrieved successfully")
    except Exception as e:
        print_error(f"Failed to get agent status: {e}")
        return False
    
    # Test 2: Roadmap Creation
    print_separator("2. ROADMAP CREATION TEST")
    try:
        user_info = {
            "interests": ["Python", "Web Development", "Data Science"],
            "skill_level": "intermediate",
            "learning_goals": ["Full-stack development", "Machine learning basics"],
            "available_hours_per_week": 15,
            "target_timeline_months": 8
        }
        
        print_info("Creating roadmap with LangChain agent...")
        result = await langchain_roadmap_agent.create_roadmap(user_info)
        
        if result.get("success"):
            roadmap_id = result["roadmap_id"]
            roadmap = result["roadmap"]
            
            print_success(f"Roadmap created successfully: {roadmap_id}")
            print_info(f"Title: {roadmap.get('title', 'N/A')}")
            print_info(f"Modules: {len(roadmap.get('modules', []))}")
            print_info(f"Duration: {roadmap.get('estimated_duration_weeks', 0)} weeks")
            
            # Save roadmap ID for later tests
            test_roadmap_id = roadmap_id
        else:
            print_error(f"Roadmap creation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print_error(f"Roadmap creation test failed: {e}")
        return False
    
    # Test 3: Roadmap Analysis
    print_separator("3. ROADMAP ANALYSIS TEST")
    try:
        print_info("Analyzing roadmap with LangChain agent...")
        analysis_result = await langchain_roadmap_agent.analyze_roadmap(test_roadmap_id)
        
        if analysis_result.get("success"):
            print_success("Roadmap analysis completed successfully")
            analysis = analysis_result.get("analysis", {})
            if isinstance(analysis, dict):
                print_info(f"Analysis keys: {list(analysis.keys())}")
            else:
                print_info("Analysis result received")
        else:
            print_error(f"Roadmap analysis failed: {analysis_result.get('error')}")
            
    except Exception as e:
        print_error(f"Roadmap analysis test failed: {e}")
    
    # Test 4: Agent Manager Integration
    print_separator("4. AGENT MANAGER INTEGRATION TEST")
    try:
        # Check if LangChain agent is registered
        langchain_agent = agent_manager.get_agent("LangChainRoadmapAgent")
        if langchain_agent:
            print_success("LangChain agent is registered in agent manager")
            
            # Test task execution through manager
            task = {
                "type": "create_roadmap",
                "user_info": {
                    "interests": ["JavaScript", "React"],
                    "skill_level": "beginner",
                    "learning_goals": ["Frontend development"],
                    "available_hours_per_week": 10,
                    "target_timeline_months": 6
                }
            }
            
            print_info("Testing task execution through agent manager...")
            manager_result = await agent_manager.execute_task(task)
            
            if manager_result.get("success"):
                print_success("Task executed successfully through agent manager")
                print_info(f"Agent used: {manager_result.get('agent')}")
                print_info(f"Framework: {manager_result.get('framework')}")
                print_info(f"Execution time: {manager_result.get('execution_time', 0):.2f}s")
            else:
                print_error(f"Task execution failed: {manager_result.get('error')}")
        else:
            print_error("LangChain agent not found in agent manager")
            
    except Exception as e:
        print_error(f"Agent manager integration test failed: {e}")
    
    # Test 5: System Status
    print_separator("5. SYSTEM STATUS TEST")
    try:
        system_status = agent_manager.get_system_status()
        print_info(f"Total Agents: {system_status['total_agents']}")
        print_info(f"Active Agents: {system_status['active_agents']}")
        print_info(f"Success Rate: {system_status['success_rate']}%")
        print_info(f"Framework Distribution: {system_status['framework_distribution']}")
        print_success("System status retrieved successfully")
        
    except Exception as e:
        print_error(f"System status test failed: {e}")
    
    # Test 6: Roadmap Retrieval
    print_separator("6. ROADMAP RETRIEVAL TEST")
    try:
        all_roadmaps = langchain_roadmap_agent.get_all_roadmaps()
        print_info(f"Total roadmaps created: {len(all_roadmaps)}")
        
        if all_roadmaps:
            for roadmap_id, roadmap in all_roadmaps.items():
                print_info(f"Roadmap ID: {roadmap_id}")
                print_info(f"  Title: {roadmap.get('title', 'N/A')}")
                print_info(f"  Modules: {len(roadmap.get('modules', []))}")
        
        print_success("Roadmap retrieval test completed")
        
    except Exception as e:
        print_error(f"Roadmap retrieval test failed: {e}")
    
    return True

async def test_performance():
    """Test agent performance"""
    print_separator("PERFORMANCE TEST")
    
    try:
        user_info = {
            "interests": ["Python", "AI"],
            "skill_level": "advanced",
            "learning_goals": ["Deep learning", "NLP"],
            "available_hours_per_week": 20,
            "target_timeline_months": 12
        }
        
        print_info("Testing performance with complex roadmap...")
        start_time = datetime.now()
        
        result = await langchain_roadmap_agent.create_roadmap(user_info)
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        if result.get("success"):
            print_success(f"Performance test completed in {execution_time:.2f} seconds")
            print_info(f"Roadmap ID: {result['roadmap_id']}")
        else:
            print_error(f"Performance test failed: {result.get('error')}")
            
    except Exception as e:
        print_error(f"Performance test failed: {e}")

async def main():
    """Main test function"""
    print("🚀 Starting LangChain Agent Tests")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Basic functionality tests
        success = await test_langchain_agent()
        
        if success:
            # Performance test
            await test_performance()
        
        print_separator("TEST SUMMARY")
        print_success("LangChain agent tests completed!")
        print_info("Check the results above for any issues.")
        
    except Exception as e:
        print_error(f"Test execution failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
