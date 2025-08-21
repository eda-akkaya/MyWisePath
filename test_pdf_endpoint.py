#!/usr/bin/env python3
"""
PDF Endpoint Test Script
"""

import requests
import json

def test_pdf_endpoint():
    """PDF endpoint'ini test et"""
    
    # Test verisi
    test_data = {
        "total_roadmaps": 2,
        "total_completed_modules": 3,
        "total_time_spent_minutes": 120,
        "overall_completion_rate": 75,
        "roadmaps": [
            {
                "roadmap_id": "test_1",
                "overall_progress": 80,
                "completed_modules": 2,
                "total_modules": 4,
                "total_time_spent_minutes": 60
            }
        ]
    }
    
    try:
        # PDF endpoint'ine istek gönder
        response = requests.post(
            "http://localhost:8000/api/v1/rag/generate-pdf/progress",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ PDF endpoint başarıyla çalışıyor!")
            
            # PDF dosyasını kaydet
            with open("test_progress_report.pdf", "wb") as f:
                f.write(response.content)
            print("📄 PDF dosyası 'test_progress_report.pdf' olarak kaydedildi")
            
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend'e bağlanılamıyor. Backend'in çalıştığından emin olun.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    test_pdf_endpoint()
