"""
Recommendation Service - Tavsiye sistemi için akıllı öneriler
"""

import os
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta

from .search_service import SearchService

logger = logging.getLogger(__name__)

class RecommendationService:
    """Tavsiye sistemi servisi"""
    
    def __init__(self, search_service: SearchService):
        """
        Args:
            search_service: Search service instance
        """
        self.search_service = search_service
        
        logger.info("Recommendation service başlatıldı")
    
    def get_learning_recommendations(self, 
                                   user_interests: List[str],
                                   user_level: str = "beginner",
                                   max_recommendations: int = 5) -> List[Dict[str, Any]]:
        """
        Kullanıcının ilgi alanlarına göre öğrenme tavsiyeleri
        
        Args:
            user_interests: Kullanıcının ilgi alanları
            user_level: Kullanıcı seviyesi (beginner, intermediate, advanced)
            max_recommendations: Maksimum tavsiye sayısı
            
        Returns:
            Tavsiye listesi
        """
        try:
            logger.info(f"Öğrenme tavsiyeleri oluşturuluyor: {user_interests}")
            
            recommendations = []
            
            for interest in user_interests:
                # İlgi alanına göre roadmap araması
                roadmap_results = self.search_service.search_roadmaps(
                    query=interest,
                    k=3
                )
                
                for result in roadmap_results:
                    recommendation = {
                        "type": "roadmap",
                        "title": result["metadata"].get("roadmap_title", "Roadmap"),
                        "content": result["content"][:200] + "...",
                        "relevance_score": result["similarity_score"],
                        "source": result["source"],
                        "interest": interest,
                        "level": user_level,
                        "action": "roadmap_detay"
                    }
                    recommendations.append(recommendation)
                
                # İlgi alanına göre eğitim içeriği araması
                content_results = self.search_service.search_educational_content(
                    query=interest,
                    k=2
                )
                
                for result in content_results:
                    recommendation = {
                        "type": "educational_content",
                        "title": f"{interest} Eğitim İçeriği",
                        "content": result["content"][:200] + "...",
                        "relevance_score": result["similarity_score"],
                        "source": result["source"],
                        "interest": interest,
                        "level": user_level,
                        "action": "content_okuma"
                    }
                    recommendations.append(recommendation)
            
            # Skorlara göre sırala ve en iyi sonuçları döndür
            recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return recommendations[:max_recommendations]
            
        except Exception as e:
            logger.error(f"Öğrenme tavsiyesi oluşturma hatası: {e}")
            return []
    
    def get_next_steps_recommendations(self, 
                                     current_roadmap_id: str,
                                     completed_modules: List[str],
                                     user_progress: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Mevcut roadmap'teki ilerlemeye göre sonraki adım tavsiyeleri
        
        Args:
            current_roadmap_id: Mevcut roadmap ID
            completed_modules: Tamamlanan modüller
            user_progress: Kullanıcı ilerleme bilgileri
            
        Returns:
            Sonraki adım tavsiyeleri
        """
        try:
            logger.info(f"Sonraki adım tavsiyeleri: {current_roadmap_id}")
            
            recommendations = []
            
            # Tamamlanan modüllere göre sonraki modül önerileri
            for module in completed_modules:
                # Modül tamamlandıktan sonra ne yapılacağını ara
                next_steps_query = f"sonraki adım {module} devam et"
                results = self.search_service.search_roadmaps(
                    query=next_steps_query,
                    k=3
                )
                
                for result in results:
                    if result["metadata"].get("roadmap_id") == current_roadmap_id:
                        recommendation = {
                            "type": "next_step",
                            "title": f"{module} Sonrası",
                            "content": result["content"][:200] + "...",
                            "relevance_score": result["similarity_score"],
                            "source": result["source"],
                            "completed_module": module,
                            "action": "modul_devam"
                        }
                        recommendations.append(recommendation)
            
            # İlerleme hızına göre tavsiyeler
            progress_rate = user_progress.get("completion_rate", 0)
            if progress_rate < 30:
                recommendations.append({
                    "type": "motivation",
                    "title": "Başlangıç Motivasyonu",
                    "content": "Yeni başladığınız yolculukta size yardımcı olacak kaynaklar...",
                    "relevance_score": 0.9,
                    "source": "system",
                    "action": "motivasyon_artir"
                })
            elif progress_rate > 70:
                recommendations.append({
                    "type": "advanced",
                    "title": "İleri Seviye İçerikler",
                    "content": "Bilginizi derinleştirmek için ileri seviye kaynaklar...",
                    "relevance_score": 0.9,
                    "source": "system",
                    "action": "ileri_seviye"
                })
            
            return recommendations[:5]
            
        except Exception as e:
            logger.error(f"Sonraki adım tavsiyesi oluşturma hatası: {e}")
            return []
    
    def get_personalized_content(self, 
                               user_profile: Dict[str, Any],
                               learning_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Kullanıcı profiline göre kişiselleştirilmiş içerik
        
        Args:
            user_profile: Kullanıcı profili
            learning_history: Öğrenme geçmişi
            
        Returns:
            Kişiselleştirilmiş içerik listesi
        """
        try:
            logger.info("Kişiselleştirilmiş içerik oluşturuluyor")
            
            recommendations = []
            
            # Kullanıcı seviyesine göre içerik
            user_level = user_profile.get("level", "beginner")
            interests = user_profile.get("interests", [])
            
            # Seviyeye uygun içerik ara
            level_query = f"{user_level} seviye öğrenme"
            level_results = self.search_service.search_educational_content(
                query=level_query,
                k=3
            )
            
            for result in level_results:
                recommendation = {
                    "type": "level_based",
                    "title": f"{user_level.title()} Seviye İçerik",
                    "content": result["content"][:200] + "...",
                    "relevance_score": result["similarity_score"],
                    "source": result["source"],
                    "user_level": user_level,
                    "action": "seviye_icerik"
                }
                recommendations.append(recommendation)
            
            # Öğrenme geçmişine göre benzer içerikler
            if learning_history:
                recent_topics = [item.get("topic", "") for item in learning_history[-3:]]
                for topic in recent_topics:
                    if topic:
                        topic_results = self.search_service.search_educational_content(
                            query=topic,
                            k=2
                        )
                        
                        for result in topic_results:
                            recommendation = {
                                "type": "history_based",
                                "title": f"{topic} İle İlgili",
                                "content": result["content"][:200] + "...",
                                "relevance_score": result["similarity_score"],
                                "source": result["source"],
                                "related_topic": topic,
                                "action": "benzer_icerik"
                            }
                            recommendations.append(recommendation)
            
            return recommendations[:5]
            
        except Exception as e:
            logger.error(f"Kişiselleştirilmiş içerik oluşturma hatası: {e}")
            return []
    
    def get_daily_recommendations(self, 
                                user_id: str,
                                date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Günlük tavsiyeler
        
        Args:
            user_id: Kullanıcı ID
            date: Tarih (opsiyonel, bugün varsayılan)
            
        Returns:
            Günlük tavsiye listesi
        """
        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            
            logger.info(f"Günlük tavsiyeler: {user_id} - {date}")
            
            # Basit günlük tavsiyeler (gerçek uygulamada kullanıcı verilerine göre)
            daily_recommendations = [
                {
                    "type": "daily_tip",
                    "title": "Günün İpucu",
                    "content": "Bugün 30 dakika yeni bir konu öğrenmeye ayırın. Küçük adımlar büyük sonuçlar getirir!",
                    "relevance_score": 0.8,
                    "source": "system",
                    "date": date,
                    "action": "gunluk_ipucu"
                },
                {
                    "type": "motivation",
                    "title": "Motivasyon Mesajı",
                    "content": "Her gün öğrendiğiniz yeni bir şey, gelecekteki başarınızın temelidir.",
                    "relevance_score": 0.7,
                    "source": "system",
                    "date": date,
                    "action": "motivasyon"
                }
            ]
            
            # Rastgele bir konu önerisi
            random_topics = ["Python programlama", "Web geliştirme", "Veri analizi", "Yapay zeka"]
            import random
            random_topic = random.choice(random_topics)
            
            topic_results = self.search_service.search_educational_content(
                query=random_topic,
                k=1
            )
            
            if topic_results:
                daily_recommendations.append({
                    "type": "discovery",
                    "title": "Keşfet: " + random_topic,
                    "content": topic_results[0]["content"][:200] + "...",
                    "relevance_score": topic_results[0]["similarity_score"],
                    "source": topic_results[0]["source"],
                    "date": date,
                    "action": "yeni_konu_kesfet"
                })
            
            return daily_recommendations
            
        except Exception as e:
            logger.error(f"Günlük tavsiye oluşturma hatası: {e}")
            return []
    
    def get_related_content(self, 
                          content_id: str,
                          content_type: str,
                          max_related: int = 3) -> List[Dict[str, Any]]:
        """
        Belirli bir içerikle ilgili diğer içerikler
        
        Args:
            content_id: İçerik ID
            content_type: İçerik türü
            max_related: Maksimum ilgili içerik sayısı
            
        Returns:
            İlgili içerik listesi
        """
        try:
            logger.info(f"İlgili içerik aranıyor: {content_id} - {content_type}")
            
            # İçerik türüne göre arama yap
            if content_type == "roadmap":
                results = self.search_service.search_roadmaps(
                    query=f"roadmap {content_id}",
                    k=max_related
                )
            elif content_type == "educational":
                results = self.search_service.search_educational_content(
                    query=f"eğitim {content_id}",
                    k=max_related
                )
            else:
                results = self.search_service.search_documents(
                    query=content_id,
                    k=max_related
                )
            
            related_content = []
            for result in results:
                content = {
                    "type": content_type,
                    "title": f"İlgili {content_type.title()}",
                    "content": result["content"][:200] + "...",
                    "relevance_score": result["similarity_score"],
                    "source": result["source"],
                    "original_content_id": content_id,
                    "action": "ilgili_icerik"
                }
                related_content.append(content)
            
            return related_content
            
        except Exception as e:
            logger.error(f"İlgili içerik arama hatası: {e}")
            return []
