#!/usr/bin/env python3
"""
Serp AI Entegrasyon Test Script'i
Bu script Serp AI entegrasyonunu test eder.
"""

import asyncio
import sys
import os

# Mevcut dizini Python path'ine ekle
sys.path.append(os.path.dirname(__file__))

from services.serp_ai_service import serp_ai_service
from services.ai_service import ai_service

async def test_serp_ai_integration():
    """Serp AI entegrasyonunu test et"""
    
    print("🔍 Serp AI Entegrasyon Testi Başlıyor...")
    print("=" * 50)
    
    # Test 1: Kavram çıkarma
    print("\n1. Kavram Çıkarma Testi:")
    test_message = "Python programlama öğrenmek istiyorum, makine öğrenmesi ve veri bilimi konularında da yardım alabilir miyim?"
    concepts = serp_ai_service.extract_learning_concepts(test_message)
    print(f"Test mesajı: {test_message}")
    print(f"Çıkarılan kavramlar: {concepts}")
    
    # Test 2: Eğitim içeriği arama
    print("\n2. Eğitim İçeriği Arama Testi:")
    try:
        results = await serp_ai_service.search_educational_content("python tutorial", "beginner", 3)
        print(f"Python tutorial araması sonuçları: {len(results)} sonuç bulundu")
        for i, result in enumerate(results[:2], 1):
            print(f"  {i}. {result['title']} ({result['platform']})")
    except Exception as e:
        print(f"  Hata: {e}")
    
    # Test 3: Trend konular
    print("\n3. Trend Konular Testi:")
    try:
        trending = await serp_ai_service.get_trending_educational_topics()
        print(f"Trend konular: {len(trending)} sonuç bulundu")
        for i, topic in enumerate(trending[:3], 1):
            print(f"  {i}. {topic['title']} ({topic['platform']})")
    except Exception as e:
        print(f"  Hata: {e}")
    
    # Test 4: AI ile entegre analiz
    print("\n4. AI ile Entegre Analiz Testi:")
    try:
        analysis = await ai_service.analyze_learning_request_with_serp(test_message)
        print(f"AI analiz sonucu: {analysis}")
    except Exception as e:
        print(f"  Hata: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Serp AI Entegrasyon Testi Tamamlandı!")

def test_concept_extraction():
    """Kavram çıkarma fonksiyonunu test et"""
    
    print("\n🧠 Kavram Çıkarma Detaylı Testi:")
    print("-" * 30)
    
    test_cases = [
        "Python öğrenmek istiyorum",
        "React ve JavaScript ile web geliştirme yapmak istiyorum",
        "Makine öğrenmesi ve yapay zeka konularında uzmanlaşmak istiyorum",
        "Docker ve Kubernetes ile DevOps öğrenmek istiyorum",
        "Veri bilimi ve istatistik konularında kendimi geliştirmek istiyorum",
        "Sadece merhaba demek istiyorum"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        concepts = serp_ai_service.extract_learning_concepts(test_case)
        print(f"{i}. '{test_case}' -> {concepts}")

if __name__ == "__main__":
    print("🚀 MyWisePath Serp AI Entegrasyon Testi")
    print("=" * 50)
    
    # Kavram çıkarma testi
    test_concept_extraction()
    
    # Asenkron testleri çalıştır
    asyncio.run(test_serp_ai_integration()) 