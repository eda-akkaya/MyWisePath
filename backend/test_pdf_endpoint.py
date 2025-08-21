#!/usr/bin/env python3
"""
PDF Endpoint Test Script
"""

import requests
import json

def test_pdf_endpoint():
    """PDF endpoint'ini test eder"""
    try:
        # Test verisi
        test_roadmap = {
            "title": "Test Roadmap",
            "description": "Bu bir test roadmap'idir",
            "modules": [
                {
                    "title": "Modül 1: Temel Kavramlar",
                    "description": "Temel kavramları öğrenin",
                    "difficulty": "Başlangıç",
                    "estimated_hours": 10,
                    "resources": ["Kurs 1", "Video 1"]
                }
            ]
        }
        
        # Authentication'ı kaldırdık, sadece content-type header'ı
        headers = {
            'Content-Type': 'application/json'
        }
        
        print("🔄 PDF endpoint test ediliyor...")
        print(f"URL: http://localhost:8000/api/v1/rag/generate-pdf/roadmap")
        print(f"Data: {json.dumps(test_roadmap, indent=2)}")
        
        # POST isteği gönder
        response = requests.post(
            'http://localhost:8000/api/v1/rag/generate-pdf/roadmap',
            headers=headers,
            json=test_roadmap,
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ PDF endpoint başarılı!")
            print(f"📁 Content-Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"📁 Content-Length: {response.headers.get('content-length', 'Unknown')}")
            
            # PDF içeriğini kontrol et
            content = response.content
            print(f"📁 Content Size: {len(content)} bytes")
            
            if len(content) > 0:
                print("✅ PDF içeriği başarıyla alındı!")
                
                # PDF'i kaydet
                with open('test_output.pdf', 'wb') as f:
                    f.write(content)
                print("💾 PDF dosyası 'test_output.pdf' olarak kaydedildi")
                return True
            else:
                print("❌ PDF içeriği boş!")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"❌ Error: {error_data}")
            except:
                print(f"❌ Error Text: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend bağlantı hatası! Backend çalışıyor mu?")
        return False
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PDF Endpoint Test Başlatılıyor...")
    success = test_pdf_endpoint()
    
    if success:
        print("\n🎉 Test başarılı! PDF endpoint çalışıyor.")
    else:
        print("\n💥 Test başarısız! PDF endpoint'inde sorun var.")
