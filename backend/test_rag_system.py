"""
RAG Sistemi Test Dosyası
Bu dosya RAG sisteminin temel bileşenlerini test eder.
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# RAG modüllerini import et
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.document_processor import DocumentProcessor
from rag.vector_store import VectorStore
from rag.search_service import SearchService
from rag.recommendation_service import RecommendationService
from rag.pdf_generator import PDFGenerator

def test_document_processor():
    """Document Processor testleri"""
    print("🔍 Document Processor Testleri...")
    
    doc_processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)
    
    # Test metni oluştur
    test_text = """
    Python Programlama Dili
    
    Python, 1991 yılında Guido van Rossum tarafından geliştirilen yüksek seviyeli bir programlama dilidir.
    Python'ın en önemli özelliklerinden biri okunabilirliğidir. Kod yazarken girintileme kullanılır.
    
    Python'da veri tipleri:
    - String: Metin verileri
    - Integer: Tam sayılar
    - Float: Ondalıklı sayılar
    - List: Liste veri yapısı
    - Dictionary: Sözlük veri yapısı
    
    Web Geliştirme:
    Python web geliştirme için birçok framework sunar:
    - Django: Tam özellikli web framework
    - Flask: Hafif web framework
    - FastAPI: Modern API framework
    
    Veri Analizi:
    Python veri analizi için güçlü kütüphaneler içerir:
    - Pandas: Veri manipülasyonu
    - NumPy: Sayısal hesaplamalar
    - Matplotlib: Veri görselleştirme
    """
    
    # Geçici dosya oluştur
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_text)
        temp_file = f.name
    
    try:
        # Metin dosyasını işle
        documents = doc_processor.process_text_file(temp_file)
        print(f"✅ Metin dosyası işlendi: {len(documents)} chunk oluşturuldu")
        
        # İlk chunk'ı kontrol et
        if documents:
            first_chunk = documents[0]
            print(f"✅ İlk chunk metadata: {first_chunk.metadata}")
            print(f"✅ İlk chunk içeriği (ilk 100 karakter): {first_chunk.page_content[:100]}...")
        
        # Blog içeriği işle
        blog_content = "<h1>Python Öğrenme Rehberi</h1><p>Bu rehber Python öğrenmek isteyenler için hazırlanmıştır.</p>"
        blog_docs = doc_processor.process_blog_content(blog_content, "python_blog")
        print(f"✅ Blog içeriği işlendi: {len(blog_docs)} chunk oluşturuldu")
        
        # Roadmap içeriği işle
        roadmap_data = {
            "id": "test_roadmap_1",
            "title": "Python Öğrenme Roadmap",
            "description": "Python programlama dilini öğrenmek için kapsamlı rehber",
            "goals": ["Temel Python syntax'ını öğren", "Web geliştirme yap", "Veri analizi öğren"],
            "modules": [
                {
                    "title": "Temel Python",
                    "description": "Python'un temel kavramları",
                    "resources": ["Python.org dokümantasyonu", "Codecademy Python kursu"]
                },
                {
                    "title": "Web Geliştirme",
                    "description": "Django ve Flask ile web geliştirme",
                    "resources": ["Django tutorial", "Flask documentation"]
                }
            ]
        }
        
        roadmap_docs = doc_processor.process_roadmap_content(roadmap_data)
        print(f"✅ Roadmap içeriği işlendi: {len(roadmap_docs)} chunk oluşturuldu")
        
    finally:
        # Geçici dosyayı sil
        os.unlink(temp_file)
    
    print("✅ Document Processor testleri tamamlandı\n")

def test_vector_store():
    """Vector Store testleri"""
    print("🗄️ Vector Store Testleri...")
    
    # Test dizini oluştur
    test_dir = "./test_vector_store"
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # Vector store'u başlat
        vector_store = VectorStore(
            store_type="chroma",
            embedding_model="huggingface",
            persist_directory=test_dir,
            collection_name="test_collection"
        )
        print("✅ Vector store başlatıldı")
        
        # Test belgeleri oluştur
        test_documents = [
            "Python programlama dili çok popülerdir.",
            "Web geliştirme için Django framework kullanılır.",
            "Veri analizi için Pandas kütüphanesi kullanılır.",
            "Machine learning için scikit-learn kütüphanesi önerilir.",
            "Python'da liste ve sözlük veri yapıları vardır."
        ]
        
        # Belgeleri ekle
        from langchain.schema import Document
        docs = []
        for i, text in enumerate(test_documents):
            doc = Document(
                page_content=text,
                metadata={"source": f"test_doc_{i}", "chunk_id": i, "file_type": "text"}
            )
            docs.append(doc)
        
        vector_store.add_documents(docs)
        print(f"✅ {len(docs)} belge vector store'a eklendi")
        
        # Arama testi
        results = vector_store.similarity_search("Python programlama", k=3)
        print(f"✅ Arama sonucu: {len(results)} sonuç bulundu")
        
        for i, result in enumerate(results):
            print(f"   Sonuç {i+1}: {result.page_content[:50]}...")
        
        # İstatistikler
        stats = vector_store.get_collection_stats()
        print(f"✅ Vector store istatistikleri: {stats}")
        
    finally:
        # Test dizinini temizle
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
    
    print("✅ Vector Store testleri tamamlandı\n")

def test_search_service():
    """Search Service testleri"""
    print("🔍 Search Service Testleri...")
    
    # Test dizini oluştur
    test_dir = "./test_search"
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # Bileşenleri başlat
        doc_processor = DocumentProcessor()
        vector_store = VectorStore(
            store_type="chroma",
            embedding_model="huggingface",
            persist_directory=test_dir
        )
        search_service = SearchService(vector_store, doc_processor)
        
        print("✅ Search service başlatıldı")
        
        # Test blog içeriği ekle
        blog_content = """
        Python Programlama Rehberi
        
        Python, öğrenmesi kolay ve güçlü bir programlama dilidir. 
        Web geliştirme, veri analizi, yapay zeka gibi alanlarda kullanılır.
        
        Django Framework:
        Django, Python'un en popüler web framework'üdür. 
        Hızlı geliştirme ve güvenlik özellikleri sunar.
        
        Veri Analizi:
        Pandas kütüphanesi ile veri analizi yapabilirsiniz.
        NumPy ile sayısal hesaplamalar gerçekleştirebilirsiniz.
        """
        
        result = search_service.add_blog_content_to_index(blog_content, "python_guide")
        print(f"✅ Blog içeriği eklendi: {result}")
        
        # Arama testi
        search_results = search_service.search_documents("Python programlama", k=3)
        print(f"✅ Arama sonucu: {len(search_results)} sonuç bulundu")
        
        for i, result in enumerate(search_results):
            print(f"   Sonuç {i+1}: {result['content'][:100]}...")
            print(f"   Skor: {result['similarity_score']:.3f}")
        
        # Bağlam alma testi
        context = search_service.get_relevant_context("web geliştirme", max_chars=500)
        print(f"✅ Bağlam alındı: {len(context)} karakter")
        print(f"   Bağlam: {context[:200]}...")
        
    finally:
        # Test dizinini temizle
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
    
    print("✅ Search Service testleri tamamlandı\n")

def test_recommendation_service():
    """Recommendation Service testleri"""
    print("💡 Recommendation Service Testleri...")
    
    # Test dizini oluştur
    test_dir = "./test_recommendations"
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # Bileşenleri başlat
        doc_processor = DocumentProcessor()
        vector_store = VectorStore(
            store_type="chroma",
            embedding_model="huggingface",
            persist_directory=test_dir
        )
        search_service = SearchService(vector_store, doc_processor)
        recommendation_service = RecommendationService(search_service)
        
        print("✅ Recommendation service başlatıldı")
        
        # Test içerikleri ekle
        test_contents = [
            "Python programlama dili öğrenme rehberi",
            "Web geliştirme için Django framework tutorial",
            "Veri analizi ve Pandas kütüphanesi kullanımı",
            "Machine learning algoritmaları ve uygulamaları",
            "React ve JavaScript ile modern web geliştirme"
        ]
        
        for i, content in enumerate(test_contents):
            search_service.add_blog_content_to_index(content, f"test_content_{i}")
        
        # Öğrenme tavsiyeleri testi
        recommendations = recommendation_service.get_learning_recommendations(
            user_interests=["Python", "Web Development"],
            user_level="beginner",
            max_recommendations=3
        )
        
        print(f"✅ Öğrenme tavsiyeleri: {len(recommendations)} tavsiye")
        for i, rec in enumerate(recommendations):
            print(f"   Tavsiye {i+1}: {rec['title']}")
            print(f"   Skor: {rec['relevance_score']:.3f}")
        
        # Günlük tavsiyeler testi
        daily_recs = recommendation_service.get_daily_recommendations("test_user")
        print(f"✅ Günlük tavsiyeler: {len(daily_recs)} tavsiye")
        
    finally:
        # Test dizinini temizle
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
    
    print("✅ Recommendation Service testleri tamamlandı\n")

def test_pdf_generator():
    """PDF Generator testleri"""
    print("📄 PDF Generator Testleri...")
    
    # Test dizini oluştur
    test_dir = "./test_pdfs"
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        pdf_generator = PDFGenerator(output_directory=test_dir)
        print("✅ PDF generator başlatıldı")
        
        # Test roadmap verisi
        test_roadmap = {
            "id": "test_roadmap_1",
            "title": "Python Öğrenme Roadmap",
            "description": "Python programlama dilini sıfırdan öğrenmek için kapsamlı rehber",
            "goals": [
                "Temel Python syntax'ını öğren",
                "Web geliştirme yapabil",
                "Veri analizi yapabil",
                "Machine learning projeleri geliştirebil"
            ],
            "modules": [
                {
                    "title": "Temel Python",
                    "description": "Python'un temel kavramları ve syntax'ı",
                    "resources": [
                        "Python.org resmi dokümantasyonu",
                        "Codecademy Python kursu",
                        "Real Python tutorials"
                    ],
                    "tasks": [
                        "İlk Python programını yaz",
                        "Değişkenler ve veri tiplerini öğren",
                        "Fonksiyonlar yaz"
                    ]
                },
                {
                    "title": "Web Geliştirme",
                    "description": "Django ve Flask ile web uygulamaları geliştirme",
                    "resources": [
                        "Django official tutorial",
                        "Flask documentation",
                        "Web development best practices"
                    ],
                    "tasks": [
                        "İlk Django projesini oluştur",
                        "Basit bir blog uygulaması yap",
                        "API endpoint'leri yaz"
                    ]
                }
            ],
            "estimated_duration": "3-6 ay",
            "difficulty": "Başlangıç"
        }
        
        # Test kullanıcı bilgileri
        test_user = {
            "name": "Test Kullanıcı",
            "email": "test@example.com"
        }
        
        # Roadmap PDF'i oluştur
        pdf_path = pdf_generator.generate_roadmap_pdf(test_roadmap, test_user)
        print(f"✅ Roadmap PDF oluşturuldu: {pdf_path}")
        
        # PDF bilgilerini al
        pdf_info = pdf_generator.get_pdf_info(pdf_path)
        print(f"✅ PDF bilgileri: {pdf_info}")
        
        # Test ilerleme verisi
        test_progress = {
            "total_roadmaps": 2,
            "total_completed_modules": 5,
            "total_time_spent_minutes": 1200,
            "overall_completion_rate": 65.5,
            "roadmaps": [
                {
                    "roadmap_id": "roadmap_1",
                    "overall_progress": 75,
                    "completed_modules": 3,
                    "total_modules": 4,
                    "total_time_spent_minutes": 600
                }
            ]
        }
        
        # İlerleme raporu PDF'i oluştur
        progress_pdf_path = pdf_generator.generate_progress_report_pdf(test_progress, test_user)
        print(f"✅ İlerleme raporu PDF oluşturuldu: {progress_pdf_path}")
        
    finally:
        # Test dizinini temizle
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
    
    print("✅ PDF Generator testleri tamamlandı\n")

def main():
    """Ana test fonksiyonu"""
    print("🚀 RAG Sistemi Testleri Başlıyor...\n")
    
    try:
        # Tüm testleri çalıştır
        test_document_processor()
        test_vector_store()
        test_search_service()
        test_recommendation_service()
        test_pdf_generator()
        
        print("🎉 Tüm testler başarıyla tamamlandı!")
        print("\n📋 Test Özeti:")
        print("✅ Document Processor - Belge işleme ve chunking")
        print("✅ Vector Store - Vektör veritabanı yönetimi")
        print("✅ Search Service - Arama ve bilgi çağırma")
        print("✅ Recommendation Service - Tavsiye sistemi")
        print("✅ PDF Generator - PDF oluşturma")
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
