#!/usr/bin/env python3
"""
PDF Generator Test Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.pdf_generator import PDFGenerator

def test_pdf_generator():
    """PDF Generator'ı test eder"""
    try:
        # PDF Generator'ı başlat
        pdf_gen = PDFGenerator()
        print("✅ PDF Generator başlatıldı")
        
        # Test roadmap verisi
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
                },
                {
                    "title": "Modül 2: İleri Seviye",
                    "description": "İleri seviye konular",
                    "difficulty": "Orta",
                    "estimated_hours": 15,
                    "resources": ["Kurs 2", "Video 2"]
                }
            ]
        }
        
        # Test kullanıcı bilgisi
        test_user = {
            "name": "Test User",
            "email": "test@example.com"
        }
        
        print("📋 Test roadmap verisi hazırlandı")
        
        # PDF oluştur
        print("🔄 PDF oluşturuluyor...")
        pdf_path = pdf_gen.generate_roadmap_pdf(
            roadmap_data=test_roadmap,
            user_info=test_user
        )
        
        print(f"✅ PDF başarıyla oluşturuldu: {pdf_path}")
        
        # Dosyanın var olup olmadığını kontrol et
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"📁 Dosya boyutu: {file_size} bytes")
            
            if file_size > 0:
                print("✅ PDF dosyası başarıyla oluşturuldu ve boş değil!")
                return True
            else:
                print("❌ PDF dosyası boş!")
                return False
        else:
            print("❌ PDF dosyası oluşturulamadı!")
            return False
            
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 PDF Generator Test Başlatılıyor...")
    success = test_pdf_generator()
    
    if success:
        print("\n🎉 Test başarılı! PDF Generator çalışıyor.")
    else:
        print("\n💥 Test başarısız! PDF Generator'da sorun var.")
        sys.exit(1)
