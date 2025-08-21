#!/usr/bin/env python3
"""
Test Script for RoadmapAgent
Demonstrates the AI-powered learning roadmap generation capabilities
"""

import asyncio
import json
from datetime import datetime

# Import the agent system
from agents.roadmap_agent import roadmap_agent
from agents.agent_manager import agent_manager

def print_separator(title=""):
    """Print a formatted separator"""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("="*60)

def print_json(data, title=""):
    """Print JSON data in a formatted way"""
    if title:
        print(f"\n{title}:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

async def test_roadmap_agent():
    """Test the RoadmapAgent functionality"""
    
    print_separator("🚀 ROADMAP AGENT TEST BAŞLATILIYOR")
    
    # Test 1: Agent Status
    print_separator("1. Agent Durumu")
    status = roadmap_agent.get_status()
    print_json(status, "RoadmapAgent Status")
    
    # Test 2: Create Python Roadmap
    print_separator("2. Python Yol Haritası Oluşturma")
    
    python_task = {
        "type": "create_roadmap",
        "user_info": {
            "interests": ["Python", "programlama", "web geliştirme"],
            "skill_level": "beginner",
            "learning_goals": ["Python temellerini öğrenmek", "Web uygulaması geliştirmek"],
            "available_hours_per_week": 15,
            "target_timeline_months": 6
        }
    }
    
    print("Python roadmap oluşturuluyor...")
    result = await roadmap_agent.execute_task(python_task)
    print_json(result, "Python Roadmap Result")
    
    # Test 3: Create Data Science Roadmap
    print_separator("3. Veri Bilimi Yol Haritası Oluşturma")
    
    data_science_task = {
        "type": "create_roadmap",
        "user_info": {
            "interests": ["veri bilimi", "makine öğrenmesi", "Python"],
            "skill_level": "intermediate",
            "learning_goals": ["Veri analizi yapmak", "ML modelleri geliştirmek"],
            "available_hours_per_week": 20,
            "target_timeline_months": 8
        }
    }
    
    print("Data Science roadmap oluşturuluyor...")
    result = await roadmap_agent.execute_task(data_science_task)
    print_json(result, "Data Science Roadmap Result")
    
    # Test 4: Analyze Roadmap
    print_separator("4. Yol Haritası Analizi")
    
    # Get the first roadmap for analysis
    roadmaps = roadmap_agent.get_all_roadmaps()
    if roadmaps:
        first_roadmap_id = list(roadmaps.keys())[0]
        
        analyze_task = {
            "type": "analyze_roadmap",
            "roadmap_id": first_roadmap_id
        }
        
        print(f"Roadmap analiz ediliyor: {first_roadmap_id}")
        result = await roadmap_agent.execute_task(analyze_task)
        print_json(result, "Roadmap Analysis Result")
    
    # Test 5: Get Suggestions
    print_separator("5. Yol Haritası Önerileri")
    
    suggest_task = {
        "type": "suggest_roadmap",
        "user_info": {
            "interests": ["Python", "web geliştirme"],
            "skill_level": "beginner",
            "learning_goals": ["Full-stack developer olmak"]
        },
        "current_roadmap": {
            "title": "Basic Python Path",
            "modules": [
                {"title": "Python Basics", "difficulty": "beginner"}
            ]
        }
    }
    
    print("Roadmap önerileri alınıyor...")
    result = await roadmap_agent.execute_task(suggest_task)
    print_json(result, "Roadmap Suggestions Result")
    
    # Test 6: Agent Memory
    print_separator("6. Agent Belleği")
    
    memory = roadmap_agent.get_memory(limit=5)
    print_json(memory, "Recent Memory Items")
    
    print(f"\nToplam bellek öğesi: {len(roadmap_agent.memory)}")
    
    return True

async def test_agent_manager():
    """Test the AgentManager functionality"""
    
    print_separator("🤖 AGENT MANAGER TEST BAŞLATILIYOR")
    
    # Test 1: System Status
    print_separator("1. Sistem Durumu")
    system_status = agent_manager.get_system_status()
    print_json(system_status, "System Status")
    
    # Test 2: All Agent Statuses
    print_separator("2. Tüm Agent Durumları")
    agent_statuses = agent_manager.get_all_agent_statuses()
    print_json(agent_statuses, "All Agent Statuses")
    
    # Test 3: Execute Task Through Manager
    print_separator("3. Manager Üzerinden Task Çalıştırma")
    
    web_dev_task = {
        "type": "create_roadmap",
        "user_info": {
            "interests": ["web geliştirme", "JavaScript", "React"],
            "skill_level": "beginner",
            "learning_goals": ["Modern web uygulamaları geliştirmek"],
            "available_hours_per_week": 12,
            "target_timeline_months": 4
        }
    }
    
    print("Web Development roadmap oluşturuluyor...")
    result = await agent_manager.execute_task(web_dev_task)
    print_json(result, "Manager Task Result")
    
    # Test 4: Batch Task Execution
    print_separator("4. Toplu Task Çalıştırma")
    
    batch_tasks = [
        {
            "type": "create_roadmap",
            "user_info": {
                "interests": ["mobile development"],
                "skill_level": "beginner",
                "learning_goals": ["Mobile app geliştirmek"],
                "available_hours_per_week": 10,
                "target_timeline_months": 3
            }
        },
        {
            "type": "create_roadmap",
            "user_info": {
                "interests": ["cybersecurity"],
                "skill_level": "intermediate",
                "learning_goals": ["Güvenlik testleri yapmak"],
                "available_hours_per_week": 8,
                "target_timeline_months": 5
            }
        }
    ]
    
    print("Toplu task'lar çalıştırılıyor...")
    results = await agent_manager.execute_batch_tasks(batch_tasks)
    print_json(results, "Batch Task Results")
    
    return True

async def test_roadmap_operations():
    """Test roadmap CRUD operations"""
    
    print_separator("📚 ROADMAP OPERASYONLARI TEST")
    
    # Test 1: Get All Roadmaps
    print_separator("1. Tüm Roadmap'leri Listele")
    all_roadmaps = roadmap_agent.get_all_roadmaps()
    print(f"Toplam roadmap sayısı: {len(all_roadmaps)}")
    
    if all_roadmaps:
        print("\nRoadmap ID'leri:")
        for roadmap_id in all_roadmaps.keys():
            print(f"  - {roadmap_id}")
    
    # Test 2: Get Specific Roadmap
    if all_roadmaps:
        print_separator("2. Belirli Roadmap'i Getir")
        first_roadmap_id = list(all_roadmaps.keys())[0]
        roadmap = roadmap_agent.get_roadmap(first_roadmap_id)
        
        if roadmap:
            print(f"Roadmap başlığı: {roadmap.get('title', 'N/A')}")
            print(f"Modül sayısı: {len(roadmap.get('modules', []))}")
            print(f"Tahmini süre: {roadmap.get('estimated_duration_weeks', 'N/A')} hafta")
    
    # Test 3: Roadmap Templates
    print_separator("3. Roadmap Şablonları")
    templates = roadmap_agent.roadmap_templates
    print("Mevcut şablonlar:")
    for template_name, template_info in templates.items():
        print(f"  - {template_name}: {template_info['name']}")
        print(f"    Modüller: {', '.join(template_info['modules'])}")
    
    return True

def main():
    """Main test function"""
    
    print("🎯 MyWisePath RoadmapAgent Test Suite")
    print(f"Başlangıç zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run all tests
        asyncio.run(test_roadmap_agent())
        asyncio.run(test_agent_manager())
        asyncio.run(test_roadmap_operations())
        
        print_separator("✅ TÜM TESTLER BAŞARILI")
        print("RoadmapAgent sistemi başarıyla çalışıyor!")
        
        # Final status
        print_separator("📊 FİNAL DURUM")
        final_status = agent_manager.get_system_status()
        print(f"Toplam agent sayısı: {final_status['total_agents']}")
        print(f"Aktif agent sayısı: {final_status['active_agents']}")
        print(f"Toplam çalıştırılan task: {final_status['total_tasks_executed']}")
        print(f"Başarı oranı: %{final_status['success_rate']}")
        
    except Exception as e:
        print_separator("❌ TEST HATASI")
        print(f"Hata: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print(f"\nTest bitiş zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
