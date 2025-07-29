from typing import List, Dict, Any
import random
import requests
import json
from config import GEMINI_API_KEY
import google.generativeai as genai

# Gemini API'yi yapılandır
genai.configure(api_key=GEMINI_API_KEY)

class EducationalContentService:
    def __init__(self):
        # AI model'ini başlat
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Temel eğitim platformları ve API'leri
        self.platforms = {
            "coursera": "https://www.coursera.org",
            "udemy": "https://www.udemy.com", 
            "edx": "https://www.edx.org",
            "khan_academy": "https://www.khanacademy.org",
            "freecodecamp": "https://www.freecodecamp.org",
            "datacamp": "https://www.datacamp.com",
            "pluralsight": "https://www.pluralsight.com",
            "skillshare": "https://www.skillshare.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com"
        }
        
        # Cache için basit veritabanı
        self.content_cache = {}
    
    def get_content_recommendations(self, topic: str, skill_level: str = "beginner", limit: int = 5) -> List[Dict[str, Any]]:
        """
        AI kullanarak belirli bir konu ve seviye için eğitim içerik önerileri getir
        """
        try:
            # Cache'den kontrol et
            cache_key = f"{topic}_{skill_level}_{limit}"
            if cache_key in self.content_cache:
                return self.content_cache[cache_key]
            
            # AI ile eğitim önerileri oluştur
            recommendations = self._generate_ai_recommendations(topic, skill_level, limit)
            
            # Cache'e kaydet
            self.content_cache[cache_key] = recommendations
            
            return recommendations
            
        except Exception as e:
            print(f"AI content recommendation error: {e}")
            # Fallback olarak basit öneriler döndür
            return self._get_fallback_recommendations(topic, skill_level, limit)
    
    def _generate_ai_recommendations(self, topic: str, skill_level: str, limit: int) -> List[Dict[str, Any]]:
        """
        AI kullanarak eğitim önerileri oluştur
        """
        if not GEMINI_API_KEY:
            # Anahtar yoksa fallback veya hata
            pass
        
        try:
            # AI prompt'u oluştur
            prompt = f"""
            Aşağıdaki konu ve seviye için {limit} adet eğitim kaynağı öner:
            
            Konu: {topic}
            Seviye: {skill_level}
            
            Her öneri için şu bilgileri ver:
            - title: Eğitim başlığı
            - platform: Platform adı (Coursera, Udemy, freeCodeCamp, YouTube, GitHub, vb.)
            - url: Gerçek URL (mümkünse)
            - type: course, tutorial, video, book, project
            - duration: Tahmini süre
            - rating: 4.0-5.0 arası rating
            - description: Kısa açıklama
            
            Sadece JSON formatında cevap ver:
            [
                {{
                    "title": "Başlık",
                    "platform": "Platform",
                    "url": "https://example.com",
                    "type": "course",
                    "duration": "20 saat",
                    "rating": 4.5,
                    "description": "Açıklama"
                }}
            ]
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # JSON'u parse et
            try:
                # JSON bloğunu bul
                import re
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    recommendations = json.loads(json_match.group())
                    return recommendations[:limit]
                else:
                    raise ValueError("JSON bulunamadı")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON parse error: {e}")
                return self._get_fallback_recommendations(topic, skill_level, limit)
                
        except Exception as e:
            print(f"AI recommendation error: {e}")
            return self._get_fallback_recommendations(topic, skill_level, limit)
    
    def _get_fallback_recommendations(self, topic: str, skill_level: str, limit: int) -> List[Dict[str, Any]]:
        """
        AI çalışmadığında fallback öneriler döndür
        """
        topic_lower = topic.lower()
        
        # Konuya göre öneriler
        if "python" in topic_lower:
            return [
                {
                    "title": "Python Temelleri - Sıfırdan Başlayın",
                    "platform": "Python.org",
                    "url": "https://docs.python.org/3/tutorial/",
                    "type": "tutorial",
                    "duration": "20 saat",
                    "rating": 4.8,
                    "description": "Python'un resmi tutorial'ı"
                },
                {
                    "title": "Python for Everybody",
                    "platform": "Coursera",
                    "url": "https://www.coursera.org/specializations/python",
                    "type": "course",
                    "duration": "40 saat",
                    "rating": 4.7,
                    "description": "Michigan Üniversitesi'nden Python kursu"
                },
                {
                    "title": "Learn Python - Free Interactive Tutorial",
                    "platform": "LearnPython.org",
                    "url": "https://www.learnpython.org/",
                    "type": "interactive",
                    "duration": "15 saat",
                    "rating": 4.6,
                    "description": "İnteraktif Python öğrenme platformu"
                }
            ][:limit]
        
        elif "javascript" in topic_lower:
            return [
                {
                    "title": "JavaScript Tutorial",
                    "platform": "MDN Web Docs",
                    "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
                    "type": "tutorial",
                    "duration": "25 saat",
                    "rating": 4.8,
                    "description": "Mozilla'nın kapsamlı JavaScript rehberi"
                },
                {
                    "title": "JavaScript Fundamentals",
                    "platform": "freeCodeCamp",
                    "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
                    "type": "course",
                    "duration": "35 saat",
                    "rating": 4.6,
                    "description": "Ücretsiz JavaScript algoritma kursu"
                }
            ][:limit]
        
        elif "react" in topic_lower:
            return [
                {
                    "title": "React Tutorial",
                    "platform": "React Documentation",
                    "url": "https://react.dev/learn",
                    "type": "tutorial",
                    "duration": "30 saat",
                    "rating": 4.9,
                    "description": "React'in resmi öğrenme rehberi"
                },
                {
                    "title": "React for Beginners",
                    "platform": "Udemy",
                    "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
                    "type": "course",
                    "duration": "45 saat",
                    "rating": 4.7,
                    "description": "Kapsamlı React kursu"
                }
            ][:limit]
        
        else:
            # Genel programlama önerileri
            return [
                {
                    "title": "Programming Fundamentals",
                    "platform": "freeCodeCamp",
                    "url": "https://www.freecodecamp.org/learn/responsive-web-design/",
                    "type": "course",
                    "duration": "30 saat",
                    "rating": 4.6,
                    "description": "Web geliştirme temelleri"
                },
                {
                    "title": "Computer Science Fundamentals",
                    "platform": "Khan Academy",
                    "url": "https://www.khanacademy.org/computing/computer-science",
                    "type": "course",
                    "duration": "40 saat",
                    "rating": 4.5,
                    "description": "Bilgisayar bilimi temelleri"
                },
                {
                    "title": "Programming for Everybody",
                    "platform": "Coursera",
                    "url": "https://www.coursera.org/learn/python",
                    "type": "course",
                    "duration": "35 saat",
                    "rating": 4.7,
                    "description": "Herkes için programlama"
                }
            ][:limit]
    
    def search_content(self, query: str, skill_level: str = "beginner", limit: int = 5) -> List[Dict[str, Any]]:
        """
        AI kullanarak içerik arama
        """
        try:
            # AI ile arama yap
            prompt = f"""
            "{query}" konusu için {skill_level} seviyede {limit} adet eğitim kaynağı ara ve öner.
            
            Her öneri için şu bilgileri ver:
            - title: Eğitim başlığı
            - platform: Platform adı
            - url: Gerçek URL
            - type: course, tutorial, video, book, project
            - duration: Tahmini süre
            - rating: 4.0-5.0 arası rating
            - description: Kısa açıklama
            
            Sadece JSON formatında cevap ver:
            [
                {{
                    "title": "Başlık",
                    "platform": "Platform",
                    "url": "https://example.com",
                    "type": "course",
                    "duration": "20 saat",
                    "rating": 4.5,
                    "description": "Açıklama"
                }}
            ]
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # JSON'u parse et
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group())
                return results[:limit]
            else:
                return self._get_fallback_recommendations(query, skill_level, limit)
                
        except Exception as e:
            print(f"AI search error: {e}")
            return self._get_fallback_recommendations(query, skill_level, limit)
    
    def get_popular_content(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        AI kullanarak popüler içerikleri getir
        """
        try:
            # AI ile popüler içerikleri öner
            prompt = f"""
            Şu anda en popüler {limit} adet programlama ve teknoloji eğitim kaynağını öner.
            
            Her öneri için şu bilgileri ver:
            - title: Eğitim başlığı
            - platform: Platform adı
            - url: Gerçek URL
            - type: course, tutorial, video, book, project
            - duration: Tahmini süre
            - rating: 4.0-5.0 arası rating
            - description: Kısa açıklama
            
            Sadece JSON formatında cevap ver:
            [
                {{
                    "title": "Başlık",
                    "platform": "Platform",
                    "url": "https://example.com",
                    "type": "course",
                    "duration": "20 saat",
                    "rating": 4.5,
                    "description": "Açıklama"
                }}
            ]
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # JSON'u parse et
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group())
                return results[:limit]
            else:
                return self._get_fallback_recommendations("programming", "beginner", limit)
                
        except Exception as e:
            print(f"AI popular content error: {e}")
            return self._get_fallback_recommendations("programming", "beginner", limit)

# Global service instance
educational_content_service = EducationalContentService() 