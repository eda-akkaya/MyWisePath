import requests
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import asyncio
import aiohttp
from config import GEMINI_API_KEY
import google.generativeai as genai

# Gemini API'yi yapılandır
genai.configure(api_key=GEMINI_API_KEY)

class LiveContentService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Eğitim platformları ve API endpoint'leri
        self.platforms = {
            "coursera": {
                "search_url": "https://www.coursera.org/search",
                "api_url": "https://www.coursera.org/api/searchQuery"
            },
            "udemy": {
                "search_url": "https://www.udemy.com/courses/search/",
                "api_url": "https://www.udemy.com/api-2.0/search-courses/"
            },
            "edx": {
                "search_url": "https://www.edx.org/search",
                "api_url": "https://www.edx.org/api/v1/catalog/search"
            },
            "freecodecamp": {
                "search_url": "https://www.freecodecamp.org/news/search/",
                "api_url": "https://www.freecodecamp.org/api/articles"
            },
            "github": {
                "search_url": "https://github.com/search",
                "api_url": "https://api.github.com/search/repositories"
            },
            "youtube": {
                "search_url": "https://www.youtube.com/results",
                "api_url": "https://www.googleapis.com/youtube/v3/search"
            }
        }
        
        # Cache için
        self.cache = {}
        self.cache_duration = 3600  # 1 saat
    
    async def search_live_content(self, topic: str, skill_level: str = "beginner", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Gerçek zamanlı internet araştırması yaparak eğitim içerikleri bul
        """
        try:
            # Cache kontrolü
            cache_key = f"{topic}_{skill_level}_{limit}"
            if cache_key in self.cache:
                cache_time, cached_data = self.cache[cache_key]
                if time.time() - cache_time < self.cache_duration:
                    return cached_data
            
            # Paralel olarak birden fazla platform'dan arama yap
            tasks = [
                self._search_coursera(topic, skill_level),
                self._search_udemy(topic, skill_level),
                self._search_freecodecamp(topic, skill_level),
                self._search_github(topic, skill_level),
                self._search_youtube(topic, skill_level)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Sonuçları birleştir ve sırala
            all_results = []
            for result in results:
                if isinstance(result, list):
                    all_results.extend(result)
            
            # AI ile sonuçları analiz et ve en iyilerini seç
            final_results = await self._ai_analyze_and_rank(all_results, topic, skill_level, limit)
            
            # Cache'e kaydet
            self.cache[cache_key] = (time.time(), final_results)
            
            return final_results
            
        except Exception as e:
            print(f"Live content search error: {e}")
            return await self._get_fallback_content(topic, skill_level, limit)
    
    async def _search_coursera(self, topic: str, skill_level: str) -> List[Dict[str, Any]]:
        """Coursera'dan içerik ara"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://www.coursera.org/api/searchQuery"
                params = {
                    "query": topic,
                    "limit": 20,
                    "start": 0
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        courses = data.get('linked', {}).get('onDemandCourseV2s', [])
                        
                        results = []
                        for course in courses[:5]:
                            results.append({
                                "title": course.get('name', ''),
                                "platform": "Coursera",
                                "url": f"https://www.coursera.org/learn/{course.get('slug', '')}",
                                "type": "course",
                                "duration": f"{course.get('duration', 0)} saat",
                                "rating": course.get('averageFiveStarRating', 4.0),
                                "description": course.get('description', ''),
                                "instructor": course.get('instructorIds', []),
                                "language": course.get('language', 'English'),
                                "price": "Ücretsiz" if course.get('isFree', False) else "Ücretli"
                            })
                        return results
        except Exception as e:
            print(f"Coursera search error: {e}")
        return []
    
    async def _search_udemy(self, topic: str, skill_level: str) -> List[Dict[str, Any]]:
        """Udemy'den içerik ara"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://www.udemy.com/api-2.0/search-courses/"
                params = {
                    "q": topic,
                    "ordering": "relevance",
                    "page_size": 10
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        courses = data.get('results', [])
                        
                        results = []
                        for course in courses[:5]:
                            results.append({
                                "title": course.get('title', ''),
                                "platform": "Udemy",
                                "url": f"https://www.udemy.com{course.get('url', '')}",
                                "type": "course",
                                "duration": f"{course.get('content_info', '')}",
                                "rating": course.get('rating', 4.0),
                                "description": course.get('headline', ''),
                                "instructor": course.get('instructor_name', ''),
                                "language": course.get('locale', {}).get('title', 'English'),
                                "price": f"${course.get('price', 0)}"
                            })
                        return results
        except Exception as e:
            print(f"Udemy search error: {e}")
        return []
    
    async def _search_freecodecamp(self, topic: str, skill_level: str) -> List[Dict[str, Any]]:
        """freeCodeCamp'den içerik ara"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://www.freecodecamp.org/api/articles"
                params = {
                    "query": topic,
                    "limit": 10
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get('data', [])
                        
                        results = []
                        for article in articles[:5]:
                            results.append({
                                "title": article.get('title', ''),
                                "platform": "freeCodeCamp",
                                "url": f"https://www.freecodecamp.org/news/{article.get('slug', '')}",
                                "type": "tutorial",
                                "duration": "Okuma süresi: 10-30 dakika",
                                "rating": 4.5,
                                "description": article.get('description', ''),
                                "author": article.get('author', {}).get('name', ''),
                                "language": "English",
                                "price": "Ücretsiz"
                            })
                        return results
        except Exception as e:
            print(f"freeCodeCamp search error: {e}")
        return []
    
    async def _search_github(self, topic: str, skill_level: str) -> List[Dict[str, Any]]:
        """GitHub'dan proje ara"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.github.com/search/repositories"
                params = {
                    "q": f"{topic} tutorial learning",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 10
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        repos = data.get('items', [])
                        
                        results = []
                        for repo in repos[:5]:
                            results.append({
                                "title": repo.get('name', ''),
                                "platform": "GitHub",
                                "url": repo.get('html_url', ''),
                                "type": "project",
                                "duration": "Proje süresi: Değişken",
                                "rating": min(5.0, repo.get('stargazers_count', 0) / 1000 + 4.0),
                                "description": repo.get('description', ''),
                                "author": repo.get('owner', {}).get('login', ''),
                                "language": repo.get('language', ''),
                                "price": "Ücretsiz",
                                "stars": repo.get('stargazers_count', 0)
                            })
                        return results
        except Exception as e:
            print(f"GitHub search error: {e}")
        return []
    
    async def _search_youtube(self, topic: str, skill_level: str) -> List[Dict[str, Any]]:
        """YouTube'dan video ara"""
        try:
            # YouTube Data API key'i gerekli
            api_key = "YOUR_YOUTUBE_API_KEY"  # Gerçek uygulamada config'den alınacak
            
            async with aiohttp.ClientSession() as session:
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    "part": "snippet",
                    "q": f"{topic} tutorial {skill_level}",
                    "type": "video",
                    "order": "relevance",
                    "maxResults": 10,
                    "key": api_key
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        videos = data.get('items', [])
                        
                        results = []
                        for video in videos[:5]:
                            results.append({
                                "title": video.get('snippet', {}).get('title', ''),
                                "platform": "YouTube",
                                "url": f"https://www.youtube.com/watch?v={video.get('id', {}).get('videoId', '')}",
                                "type": "video",
                                "duration": "Video süresi: Değişken",
                                "rating": 4.3,
                                "description": video.get('snippet', {}).get('description', ''),
                                "author": video.get('snippet', {}).get('channelTitle', ''),
                                "language": "English",
                                "price": "Ücretsiz"
                            })
                        return results
        except Exception as e:
            print(f"YouTube search error: {e}")
        return []
    
    async def _ai_analyze_and_rank(self, results: List[Dict[str, Any]], topic: str, skill_level: str, limit: int) -> List[Dict[str, Any]]:
        """AI kullanarak sonuçları analiz et ve sırala"""
        try:
            if not GEMINI_API_KEY:
                # AI yoksa basit sıralama
                return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)[:limit]
            
            # AI ile analiz
            prompt = f"""
            Aşağıdaki eğitim kaynaklarını analiz et ve {topic} konusu için {skill_level} seviyede en uygun {limit} tanesini seç:
            
            Kaynaklar: {json.dumps(results, ensure_ascii=False)}
            
            Seçim kriterleri:
            1. Konuya uygunluk
            2. Seviye uygunluğu
            3. Kalite (rating)
            4. Güncellik
            5. Erişilebilirlik
            
            Sadece seçilen kaynakların JSON listesini döndür.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # JSON'u parse et
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                selected_results = json.loads(json_match.group())
                return selected_results[:limit]
            else:
                # AI çalışmazsa basit sıralama
                return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)[:limit]
                
        except Exception as e:
            print(f"AI analysis error: {e}")
            return sorted(results, key=lambda x: x.get('rating', 0), reverse=True)[:limit]
    
    async def _get_fallback_content(self, topic: str, skill_level: str, limit: int) -> List[Dict[str, Any]]:
        """Fallback içerik döndür"""
        return [
            {
                "title": f"{topic.title()} Temelleri",
                "platform": "MyWisePath",
                "url": "https://mywisepath.com",
                "type": "course",
                "duration": "20 saat",
                "rating": 4.5,
                "description": f"{topic} konusunda temel eğitim",
                "author": "MyWisePath",
                "language": "Türkçe",
                "price": "Ücretsiz"
            }
        ]
    
    async def create_dynamic_roadmap(self, topic: str, skill_level: str, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gerçek zamanlı araştırma ile dinamik roadmap oluştur
        """
        try:
            # Gerçek zamanlı içerik ara
            live_content = await self.search_live_content(topic, skill_level, 20)
            
            # AI ile roadmap oluştur
            roadmap = await self._ai_create_roadmap(topic, skill_level, live_content, user_preferences)
            
            return roadmap
            
        except Exception as e:
            print(f"Dynamic roadmap creation error: {e}")
            return await self._get_fallback_roadmap(topic, skill_level)
    
    async def _ai_create_roadmap(self, topic: str, skill_level: str, content: List[Dict[str, Any]], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """AI ile dinamik roadmap oluştur"""
        try:
            prompt = f"""
            Aşağıdaki gerçek eğitim kaynaklarını kullanarak {topic} konusu için {skill_level} seviyede bir yol haritası oluştur:
            
            Mevcut kaynaklar: {json.dumps(content, ensure_ascii=False)}
            Kullanıcı tercihleri: {json.dumps(preferences, ensure_ascii=False)}
            
            Roadmap şu yapıda olsun:
            {{
                "title": "Başlık",
                "description": "Açıklama",
                "modules": [
                    {{
                        "title": "Modül başlığı",
                        "description": "Modül açıklaması",
                        "duration": "Tahmini süre",
                        "resources": [
                            {{
                                "title": "Kaynak başlığı",
                                "platform": "Platform",
                                "url": "URL",
                                "type": "Tür",
                                "rating": 4.5
                            }}
                        ]
                    }}
                ],
                "total_duration": "Toplam süre",
                "difficulty": "Seviye",
                "prerequisites": ["Ön koşullar"],
                "learning_outcomes": ["Öğrenme çıktıları"]
            }}
            
            Sadece JSON formatında cevap ver.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # JSON'u parse et
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                roadmap = json.loads(json_match.group())
                return roadmap
            else:
                return await self._get_fallback_roadmap(topic, skill_level)
                
        except Exception as e:
            print(f"AI roadmap creation error: {e}")
            return await self._get_fallback_roadmap(topic, skill_level)
    
    async def _get_fallback_roadmap(self, topic: str, skill_level: str) -> Dict[str, Any]:
        """Fallback roadmap döndür"""
        return {
            "title": f"{topic.title()} Yol Haritası",
            "description": f"{topic} konusunda {skill_level} seviyede öğrenme yolculuğu",
            "modules": [
                {
                    "title": "Temel Kavramlar",
                    "description": f"{topic} konusunun temellerini öğrenin",
                    "duration": "10 saat",
                    "resources": [
                        {
                            "title": f"{topic.title()} Temelleri",
                            "platform": "MyWisePath",
                            "url": "https://mywisepath.com",
                            "type": "course",
                            "rating": 4.5
                        }
                    ]
                }
            ],
            "total_duration": "10 saat",
            "difficulty": skill_level,
            "prerequisites": [],
            "learning_outcomes": [f"{topic} konusunda temel bilgi sahibi olmak"]
        }

# Global service instance
live_content_service = LiveContentService() 