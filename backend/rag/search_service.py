"""
Search Service - Basit bilgi çağırma ve arama işlemleri
"""

import os
from typing import List, Dict, Any, Optional
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class SearchService:
    """Arama ve bilgi çağırma servisi - Mock verilerle çalışır"""
    
    def __init__(self):
        """Search service başlatma"""
        self.mock_data = self._load_mock_data()
        logger.info("Search service başlatıldı (mock verilerle)")
    
    def _load_mock_data(self) -> List[Dict[str, Any]]:
        """Mock arama verilerini yükler"""
        return [
            {
                "content": "Python programlama dili, web geliştirme, veri analizi ve yapay zeka alanlarında yaygın olarak kullanılır. Basit syntax'ı ve güçlü kütüphaneleri ile başlangıç seviyesi programcılar için idealdir.",
                "metadata": {
                    "source": "python_guide.pdf",
                    "file_type": "pdf",
                    "chunk_id": 1,
                    "roadmap_title": "Python Öğrenme Yolu"
                },
                "similarity_score": 0.95,
                "source": "python_guide.pdf",
                "file_type": "pdf",
                "chunk_id": 1
            },
            {
                "content": "Web geliştirme için HTML, CSS ve JavaScript temel teknolojilerdir. Modern web uygulamaları için React, Vue.js gibi framework'ler kullanılır. Backend için Node.js, Python Django veya PHP tercih edilebilir.",
                "metadata": {
                    "source": "web_development_roadmap.json",
                    "file_type": "roadmap",
                    "chunk_id": 1,
                    "roadmap_title": "Web Geliştirme Roadmap"
                },
                "similarity_score": 0.88,
                "source": "web_development_roadmap.json",
                "file_type": "roadmap",
                "chunk_id": 1
            },
            {
                "content": "Veri bilimi ve makine öğrenmesi için Python'da pandas, numpy, scikit-learn kütüphaneleri kullanılır. Jupyter Notebook'lar veri analizi için idealdir. TensorFlow ve PyTorch derin öğrenme için popülerdir.",
                "metadata": {
                    "source": "data_science_guide.pdf",
                    "file_type": "pdf",
                    "chunk_id": 2,
                    "roadmap_title": "Veri Bilimi Yolu"
                },
                "similarity_score": 0.82,
                "source": "data_science_guide.pdf",
                    "file_type": "pdf",
                "chunk_id": 2
            },
            {
                "content": "JavaScript modern web geliştirmenin temelidir. ES6+ özellikleri ile daha güçlü hale geldi. Node.js ile backend geliştirme de mümkündür. TypeScript tip güvenliği sağlar.",
                "metadata": {
                    "source": "javascript_tutorial.md",
                    "file_type": "blog",
                    "chunk_id": 1,
                    "roadmap_title": "JavaScript Öğrenme"
                },
                "similarity_score": 0.78,
                "source": "javascript_tutorial.md",
                "file_type": "blog",
                "chunk_id": 1
            },
            {
                "content": "React.js Facebook tarafından geliştirilen popüler bir JavaScript kütüphanesidir. Component tabanlı mimarisi ile yeniden kullanılabilir UI bileşenleri oluşturmayı sağlar. Virtual DOM ile performans optimizasyonu yapar.",
                "metadata": {
                    "source": "react_guide.pdf",
                    "file_type": "pdf",
                    "chunk_id": 3,
                    "roadmap_title": "React.js Öğrenme"
                },
                "similarity_score": 0.75,
                "source": "react_guide.pdf",
                "file_type": "pdf",
                "chunk_id": 3
            }
        ]
    
    def search_documents(self, 
                        query: str, 
                        k: int = 5,
                        filter_by_source: Optional[str] = None,
                        filter_by_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Belgelerde arama yapar (mock verilerle)
        
        Args:
            query: Arama sorgusu
            k: Döndürülecek sonuç sayısı
            filter_by_source: Kaynak filtreleme
            filter_by_type: Dosya türü filtreleme
            
        Returns:
            Arama sonuçları listesi
        """
        try:
            logger.info(f"Belge araması: '{query}'")
            
            # Mock verilerden filtreleme yap
            filtered_results = self.mock_data.copy()
            
            if filter_by_source:
                filtered_results = [r for r in filtered_results if filter_by_source.lower() in r["source"].lower()]
            
            if filter_by_type:
                filtered_results = [r for r in filtered_results if r["file_type"] == filter_by_type]
            
            # Basit keyword matching (gerçek uygulamada semantic search olurdu)
            query_lower = query.lower()
            scored_results = []
            
            for result in filtered_results:
                content_lower = result["content"].lower()
                score = 0
                
                # Keyword matching
                for word in query_lower.split():
                    if word in content_lower:
                        score += 0.2
                
                # Başlıkta geçiyorsa bonus puan
                if query_lower in result["metadata"].get("roadmap_title", "").lower():
                    score += 0.3
                
                if score > 0:
                    result_copy = result.copy()
                    result_copy["similarity_score"] = min(score, 1.0)
                    scored_results.append(result_copy)
            
            # Skora göre sırala
            scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            # K sayısı kadar döndür
            final_results = scored_results[:k]
            
            logger.info(f"{len(final_results)} sonuç bulundu")
            return final_results
            
        except Exception as e:
            logger.error(f"Belge arama hatası: {e}")
            return []
    
    def search_roadmaps(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Roadmap'lerde arama yapar"""
        return self.search_documents(
            query=query,
            k=k,
            filter_by_type="roadmap"
        )
    
    def search_educational_content(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Eğitim içeriklerinde arama yapar"""
        return self.search_documents(
            query=query,
            k=k,
            filter_by_type="blog"
        )
    
    def search_pdfs(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """PDF'lerde arama yapar"""
        return self.search_documents(
            query=query,
            k=k,
            filter_by_type="pdf"
        )
    
    def get_relevant_context(self, query: str, max_chars: int = 2000) -> str:
        """
        Sorgu için ilgili bağlamı döndürür
        
        Args:
            query: Sorgu
            max_chars: Maksimum karakter sayısı
            
        Returns:
            İlgili bağlam metni
        """
        try:
            # Daha fazla sonuç al
            results = self.search_documents(query, k=10)
            
            # Bağlam metnini oluştur
            context_parts = []
            current_length = 0
            
            for result in results:
                content = result["content"]
                if current_length + len(content) <= max_chars:
                    context_parts.append(content)
                    current_length += len(content)
                else:
                    # Kalan karakter sayısına göre kes
                    remaining_chars = max_chars - current_length
                    if remaining_chars > 100:  # En az 100 karakter
                        context_parts.append(content[:remaining_chars] + "...")
                    break
            
            context = "\n\n".join(context_parts)
            logger.info(f"Bağlam oluşturuldu: {len(context)} karakter")
            
            return context
            
        except Exception as e:
            logger.error(f"Bağlam oluşturma hatası: {e}")
            return ""
    
    def add_document_to_index(self, file_path: str) -> Dict[str, Any]:
        """
        Belgeyi index'e ekler (mock - gerçek işlem yapmaz)
        
        Args:
            file_path: Belge dosya yolu
            
        Returns:
            İşlem sonucu
        """
        try:
            logger.info(f"Mock belge ekleme: {file_path}")
            
            # Mock sonuç döndür
            result = {
                "success": True,
                "file_path": file_path,
                "chunks_created": 3,
                "message": "Mock: 3 chunk başarıyla eklendi"
            }
            
            logger.info(f"Mock belge eklendi: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Mock belge ekleme hatası: {e}")
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e)
            }
    
    def add_roadmap_to_index(self, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Roadmap'i index'e ekler (mock - gerçek işlem yapmaz)
        
        Args:
            roadmap_data: Roadmap verisi
            
        Returns:
            İşlem sonucu
        """
        try:
            logger.info("Mock roadmap ekleme")
            
            # Mock sonuç döndür
            result = {
                "success": True,
                "roadmap_id": roadmap_data.get("id", "mock_id"),
                "roadmap_title": roadmap_data.get("title", "Mock Roadmap"),
                "chunks_created": 5,
                "message": "Mock: Roadmap başarıyla eklendi: 5 chunk"
            }
            
            logger.info(f"Mock roadmap eklendi: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Mock roadmap ekleme hatası: {e}")
            return {
                "success": False,
                "roadmap_id": roadmap_data.get("id"),
                "error": str(e)
            }
    
    def add_blog_content_to_index(self, content: str, source: str) -> Dict[str, Any]:
        """
        Blog içeriğini index'e ekler (mock - gerçek işlem yapmaz)
        
        Args:
            content: Blog içeriği
            source: Kaynak bilgisi
            
        Returns:
            İşlem sonucu
        """
        try:
            logger.info(f"Mock blog içeriği ekleme: {source}")
            
            # Mock sonuç döndür
            result = {
                "success": True,
                "source": source,
                "chunks_created": 2,
                "message": "Mock: Blog içeriği başarıyla eklendi: 2 chunk"
            }
            
            logger.info(f"Mock blog içeriği eklendi: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Mock blog içeriği ekleme hatası: {e}")
            return {
                "success": False,
                "source": source,
                "error": str(e)
            }
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Index istatistiklerini döndürür (mock)"""
        try:
            return {
                "total_documents": len(self.mock_data),
                "document_types": {
                    "pdf": len([d for d in self.mock_data if d["file_type"] == "pdf"]),
                    "roadmap": len([d for d in self.mock_data if d["file_type"] == "roadmap"]),
                    "blog": len([d for d in self.mock_data if d["file_type"] == "blog"])
                },
                "supported_formats": ["pdf", "txt", "md", "json"],
                "mock_mode": True
            }
        except Exception as e:
            logger.error(f"Mock istatistik alma hatası: {e}")
            return {"error": str(e)}
    
    def clear_index(self) -> Dict[str, Any]:
        """Index'i temizler (mock - gerçek işlem yapmaz)"""
        try:
            logger.info("Mock index temizleme")
            return {
                "success": True,
                "message": "Mock: Index başarıyla temizlendi"
            }
        except Exception as e:
            logger.error(f"Mock index temizleme hatası: {e}")
            return {
                "success": False,
                "error": str(e)
            }
