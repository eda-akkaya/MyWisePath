#!/usr/bin/env python3
"""
Serp AI API Key Test Script'i
Bu script Serp AI API key'inizin çalışıp çalışmadığını test eder.
"""

import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

def test_serp_api_key():
    """Serp AI API key'ini test et"""
    
    print("🔑 Serp AI API Key Testi")
    print("=" * 40)
    
    # .env dosyasını yükle
    load_dotenv()
    
    # API key'i al
    api_key = os.getenv("SERP_API_KEY")
    
    if not api_key:
        print("❌ SERP_API_KEY bulunamadı!")
        print("\nÇözüm:")
        print("1. backend/.env dosyasını oluşturun")
        print("2. SERP_API_KEY=your_api_key_here satırını ekleyin")
        print("3. your_api_key_here yerine gerçek API key'inizi yazın")
        return False
    
    print(f"✅ API Key bulundu: {api_key[:10]}...")
    
    # Basit arama testi
    try:
        print("\n🔍 Test araması yapılıyor...")
        
        search_params = {
            "engine": "google",
            "q": "python tutorial",
            "api_key": api_key,
            "num": 3,
            "gl": "tr",
            "hl": "tr"
        }
        
        search = GoogleSearch(search_params)
        results = search.get_dict()
        
        if "organic_results" in results and len(results["organic_results"]) > 0:
            print("✅ API Key çalışıyor!")
            print(f"📊 {len(results['organic_results'])} sonuç bulundu")
            
            # İlk sonucu göster
            first_result = results["organic_results"][0]
            print(f"\n📝 İlk Sonuç:")
            print(f"   Başlık: {first_result.get('title', 'N/A')}")
            print(f"   URL: {first_result.get('link', 'N/A')}")
            
            return True
        else:
            print("❌ API Key çalışıyor ama sonuç bulunamadı")
            return False
            
    except Exception as e:
        print(f"❌ API Key testi başarısız: {e}")
        print("\nOlası nedenler:")
        print("1. API key yanlış olabilir")
        print("2. Aylık kullanım limiti dolmuş olabilir")
        print("3. İnternet bağlantısı sorunu olabilir")
        return False

def show_usage_info():
    """Kullanım bilgilerini göster"""
    
    print("\n📊 Serp AI Kullanım Bilgileri:")
    print("=" * 40)
    print("🆓 Ücretsiz Plan:")
    print("   - 100 arama/ay")
    print("   - Google, Bing, Yahoo")
    print("   - JSON formatında sonuçlar")
    print("\n💳 Ücretli Planlar:")
    print("   - 1,000 arama/ay: $50")
    print("   - 5,000 arama/ay: $200")
    print("   - 10,000 arama/ay: $350")
    print("\n🌐 Desteklenen Arama Motorları:")
    print("   - Google")
    print("   - Bing")
    print("   - Yahoo")
    print("   - DuckDuckGo")
    print("   - Yandex")
    print("   - Baidu")

if __name__ == "__main__":
    success = test_serp_api_key()
    
    if success:
        print("\n🎉 Serp AI API Key başarıyla çalışıyor!")
        print("Artık test script'ini çalıştırabilirsiniz:")
        print("python test_serp_ai.py")
    else:
        print("\n❌ Serp AI API Key testi başarısız!")
        print("Lütfen yukarıdaki adımları takip edin.")
    
    show_usage_info() 