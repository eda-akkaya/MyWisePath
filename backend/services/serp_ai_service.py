import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from serpapi import GoogleSearch
from config import SERP_API_KEY

class SerpAIService:
    def __init__(self):
        self.api_key = SERP_API_KEY
        self.base_url = "https://serpapi.com/search"
        
    async def search_educational_content(self, query: str, skill_level: str = "beginner", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Serp AI kullanarak eğitim içeriği ara
        """
        if not self.api_key:
            print("Serp API key ayarlanmamış")
            return []
        
        try:
            # Arama sorgusunu eğitim odaklı hale getir
            educational_query = self._enhance_query_for_education(query, skill_level)
            
            # Serp API parametreleri
            search_params = {
                "engine": "google",
                "q": educational_query,
                "api_key": self.api_key,
                "num": min(limit, 20),  # Maksimum 20 sonuç
                "gl": "tr",  # Türkiye
                "hl": "tr",  # Türkçe
                "safe": "active"
            }
            
            # Arama yap
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            # Sonuçları işle
            educational_results = []
            
            if "organic_results" in results:
                for result in results["organic_results"][:limit]:
                    # Eğitim platformlarını kontrol et
                    if self._is_educational_content(result):
                        educational_results.append({
                            "title": result.get("title", ""),
                            "url": result.get("link", ""),
                            "snippet": result.get("snippet", ""),
                            "platform": self._extract_platform(result.get("link", "")),
                            "type": self._categorize_content(result.get("title", ""), result.get("snippet", "")),
                            "skill_level": skill_level,
                            "source": "serp_ai"
                        })
            
            return educational_results
            
        except Exception as e:
            print(f"Serp AI search error: {e}")
            return []
    
    def _enhance_query_for_education(self, query: str, skill_level: str) -> str:
        """
        Sorguyu eğitim odaklı hale getir
        """
        # Eğitim platformları
        educational_platforms = [
            "coursera", "udemy", "edx", "khan academy", "freecodecamp",
            "w3schools", "mdn", "stack overflow", "github", "youtube",
            "tutorial", "course", "öğrenme", "eğitim", "ders"
        ]
        
        # Seviye bazlı anahtar kelimeler
        level_keywords = {
            "beginner": ["başlangıç", "temel", "basit", "tutorial", "öğrenme"],
            "intermediate": ["orta seviye", "ileri", "advanced", "proje"],
            "advanced": ["uzman", "expert", "ileri seviye", "profesyonel"]
        }
        
        # Sorguyu geliştir
        enhanced_query = query
        
        # Eğitim platformları ekle
        platform_keywords = " OR ".join(educational_platforms[:5])  # İlk 5 platform
        enhanced_query += f" ({platform_keywords})"
        
        # Seviye anahtar kelimeleri ekle
        if skill_level in level_keywords:
            level_keywords_str = " OR ".join(level_keywords[skill_level])
            enhanced_query += f" ({level_keywords_str})"
        
        return enhanced_query
    
    def _is_educational_content(self, result: Dict[str, Any]) -> bool:
        """
        Sonucun eğitim içeriği olup olmadığını kontrol et
        """
        url = result.get("link", "").lower()
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()
        
        # Eğitim platformları
        educational_domains = [
            "coursera.org", "udemy.com", "edx.org", "khanacademy.org",
            "freecodecamp.org", "w3schools.com", "mdn.web", "github.com",
            "youtube.com", "stackoverflow.com", "geeksforgeeks.org",
            "tutorialspoint.com", "programiz.com", "realpython.com"
        ]
        
        # Eğitim anahtar kelimeleri
        educational_keywords = [
            "tutorial", "course", "learn", "öğrenme", "eğitim", "ders",
            "guide", "how to", "nasıl", "başlangıç", "temel", "kaynak"
        ]
        
        # Domain kontrolü
        for domain in educational_domains:
            if domain in url:
                return True
        
        # Anahtar kelime kontrolü
        for keyword in educational_keywords:
            if keyword in title or keyword in snippet:
                return True
        
        return False
    
    def _extract_platform(self, url: str) -> str:
        """
        URL'den platform adını çıkar
        """
        url_lower = url.lower()
        
        platform_mapping = {
            "coursera.org": "Coursera",
            "udemy.com": "Udemy",
            "edx.org": "edX",
            "khanacademy.org": "Khan Academy",
            "freecodecamp.org": "freeCodeCamp",
            "w3schools.com": "W3Schools",
            "mdn.web": "MDN Web Docs",
            "github.com": "GitHub",
            "youtube.com": "YouTube",
            "stackoverflow.com": "Stack Overflow",
            "geeksforgeeks.org": "GeeksforGeeks",
            "tutorialspoint.com": "TutorialsPoint",
            "programiz.com": "Programiz",
            "realpython.com": "Real Python"
        }
        
        for domain, platform in platform_mapping.items():
            if domain in url_lower:
                return platform
        
        return "Web"
    
    def _categorize_content(self, title: str, snippet: str) -> str:
        """
        İçeriği kategorize et
        """
        text = (title + " " + snippet).lower()
        
        categories = {
            "video": ["video", "youtube", "tutorial video"],
            "course": ["course", "kurs", "ders", "eğitim"],
            "documentation": ["documentation", "docs", "reference", "api"],
            "tutorial": ["tutorial", "guide", "how to", "nasıl"],
            "project": ["project", "proje", "example", "örnek"],
            "article": ["article", "blog", "makale", "yazı"]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        
        return "general"
    
    async def search_multiple_topics(self, topics: List[str], skill_level: str = "beginner") -> Dict[str, List[Dict[str, Any]]]:
        """
        Birden fazla konu için aynı anda arama yap
        """
        tasks = []
        for topic in topics:
            task = self.search_educational_content(topic, skill_level, 5)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Sonuçları konu bazında grupla
        topic_results = {}
        for i, topic in enumerate(topics):
            if isinstance(results[i], list):
                topic_results[topic] = results[i]
            else:
                topic_results[topic] = []
        
        return topic_results
    
    async def get_trending_educational_topics(self) -> List[Dict[str, Any]]:
        """
        Trend olan eğitim konularını bul
        """
        trending_queries = [
            "python programming 2024",
            "machine learning tutorial",
            "web development course",
            "data science beginner",
            "react tutorial",
            "javascript es6",
            "docker tutorial",
            "git tutorial"
        ]
        
        all_results = []
        for query in trending_queries:
            results = await self.search_educational_content(query, "beginner", 3)
            all_results.extend(results)
        
        # Tekrarları kaldır ve en iyi sonuçları döndür
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result["url"] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result["url"])
        
        return unique_results[:10]  # En iyi 10 sonuç
    
    async def extract_learning_concepts(self, user_message: str) -> List[str]:
        """
        Kullanıcı mesajından öğrenme kavramlarını çıkar
        """
        # Programlama dilleri
        programming_languages = [
            "python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust",
            "swift", "kotlin", "dart", "typescript", "scala", "r", "matlab"
        ]
        
        # Teknolojiler ve framework'ler
        technologies = [
            "react", "vue", "angular", "node.js", "django", "flask", "spring",
            "express", "laravel", "asp.net", "tensorflow", "pytorch", "scikit-learn",
            "pandas", "numpy", "matplotlib", "seaborn", "docker", "kubernetes",
            "aws", "azure", "gcp", "git", "github", "sql", "mongodb", "redis"
        ]
        
        # Öğrenme alanları
        learning_areas = [
            "programlama", "web geliştirme", "mobil geliştirme", "veri bilimi",
            "makine öğrenmesi", "yapay zeka", "devops", "cybersecurity",
            "blockchain", "game development", "ui/ux", "database"
        ]
        
        # Kullanıcı mesajını küçük harfe çevir
        message_lower = user_message.lower()
        
        # Kavramları bul
        found_concepts = []
        
        # Programlama dilleri
        for lang in programming_languages:
            if lang in message_lower:
                found_concepts.append(lang)
        
        # Teknolojiler
        for tech in technologies:
            if tech in message_lower:
                found_concepts.append(tech)
        
        # Öğrenme alanları
        for area in learning_areas:
            if area in message_lower:
                found_concepts.append(area)
        
        # Eğer hiç kavram bulunamadıysa, genel terimler ara
        if not found_concepts:
            general_terms = ["öğrenmek", "başlamak", "geliştirme", "yazılım", "kod"]
            for term in general_terms:
                if term in message_lower:
                    found_concepts.append("programlama")
                    break
        
        return list(set(found_concepts))  # Tekrarları kaldır

# Global Serp AI service instance
serp_ai_service = SerpAIService() 