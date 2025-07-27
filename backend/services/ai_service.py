import google.generativeai as genai
from typing import Optional, Dict, List, Any
from config import GEMINI_API_KEY
import json
import re

# Gemini API'yi yapılandır
genai.configure(api_key=GEMINI_API_KEY)

class AIService:
    def __init__(self):
        # Gemini model'ini başlat
        self.model = genai.GenerativeModel('gemini-pro')
        
    def get_ai_response(self, user_message: str, user_context: Optional[dict] = None) -> str:
        """
        Gemini API kullanarak kullanıcı mesajına AI cevabı döndür
        """
        # API key kontrolü
        if GEMINI_API_KEY == "your_gemini_api_key_here":
            print("Gemini API key ayarlanmamış, fallback cevap döndürülüyor")
            return self.get_fallback_response(user_message)
        
        try:
            # Sistem prompt'u oluştur
            system_prompt = """Sen MyWisePath öğrenme platformunun AI asistanısın. 
            Kullanıcılara öğrenme yolculuklarında yardımcı oluyorsun.
            
            Özelliklerin:
            - Öğrenme konularında rehberlik etme
            - Yol haritası önerileri sunma
            - Programlama, veri bilimi, web geliştirme konularında bilgi verme
            - Motivasyonel ve destekleyici olma
            - Türkçe cevap verme
            - Kullanıcı isteklerini analiz edip uygun öğrenme alanlarını belirleme
            
            Kullanıcı profil bilgileri: {user_context}
            
            Eğer kullanıcı bir konu öğrenmek istiyorsa, o konuyla ilgili detaylı bilgi ver ve yol haritası oluşturma önerisi sun.
            Kısa, net ve yardımcı cevaplar ver. Maksimum 3-4 cümle."""
            
            # Kullanıcı context'ini formatla
            context_str = ""
            if user_context:
                context_str = f"Kullanıcı bilgileri: {user_context}"
            
            system_prompt = system_prompt.format(user_context=context_str)
            
            # Gemini API'ye istek gönder
            prompt = f"{system_prompt}\n\nKullanıcı: {user_message}\n\nAsistan:"
            response = self.model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini API Error: {e}")
            # Fallback cevap
            return self.get_fallback_response(user_message)

    def analyze_learning_request(self, user_message: str) -> Dict[str, Any]:
        """
        AI kullanarak kullanıcı mesajını analiz ederek öğrenme isteğini çıkarır
        """
        # API key kontrolü
        if GEMINI_API_KEY == "your_gemini_api_key_here" or not GEMINI_API_KEY:
            print("Gemini API key ayarlanmamış, basit analiz döndürülüyor")
            return self.get_simple_analysis(user_message)
        
        try:
            # AI analiz prompt'u
            analysis_prompt = f"""
            Aşağıdaki kullanıcı mesajını analiz et ve JSON formatında cevap ver:
            
            Kullanıcı mesajı: "{user_message}"
            
            Analiz etmen gereken alanlar:
            1. Öğrenme alanları (programlama, veri_bilimi, web_gelistirme, makine_ogrenmesi, mobil_gelistirme, devops)
            2. Alt konular (python, javascript, react, tensorflow, vb.)
            3. Seviye (beginner, intermediate, advanced)
            4. Zaman planı (ay cinsinden)
            5. Öğrenme isteği var mı (true/false)
            
            Sadece JSON formatında cevap ver, başka açıklama ekleme:
            {{
                "learning_areas": ["alan1", "alan2"],
                "subtopics": ["konu1", "konu2"],
                "skill_level": "beginner/intermediate/advanced",
                "timeline_months": 6,
                "has_learning_request": true/false
            }}
            """
            
            response = self.model.generate_content(analysis_prompt)
            response_text = response.text.strip()
            
            # JSON'u parse et
            try:
                # JSON bloğunu bul
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    return analysis
                else:
                    raise ValueError("JSON bulunamadı")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON parse error: {e}")
                return self.get_simple_analysis(user_message)
                
        except Exception as e:
            print(f"AI analysis error: {e}")
            return self.get_simple_analysis(user_message)

    def get_simple_analysis(self, user_message: str) -> Dict[str, Any]:
        """
        AI çalışmadığında basit kural tabanlı analiz
        """
        user_message_lower = user_message.lower()
        
        # Öğrenme alanlarını tanımla
        learning_areas = {
            "programlama": {
                "keywords": ["programlama", "kod yazma", "yazılım", "developer", "programmer"],
                "subtopics": ["python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust"]
            },
            "veri_bilimi": {
                "keywords": ["veri bilimi", "data science", "veri analizi", "data analysis", "istatistik"],
                "subtopics": ["python", "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", "pytorch"]
            },
            "web_gelistirme": {
                "keywords": ["web geliştirme", "web development", "website", "web sitesi", "frontend", "backend"],
                "subtopics": ["html", "css", "javascript", "react", "vue", "angular", "node.js", "django", "flask", "php"]
            },
            "makine_ogrenmesi": {
                "keywords": ["makine öğrenmesi", "machine learning", "yapay zeka", "artificial intelligence", "ai", "ml"],
                "subtopics": ["python", "scikit-learn", "tensorflow", "pytorch", "keras", "neural networks", "deep learning"]
            },
            "mobil_gelistirme": {
                "keywords": ["mobil uygulama", "mobile app", "android", "ios", "flutter", "react native"],
                "subtopics": ["android", "ios", "flutter", "react native", "kotlin", "swift", "dart"]
            },
            "devops": {
                "keywords": ["devops", "deployment", "ci/cd", "docker", "kubernetes", "aws", "azure"],
                "subtopics": ["docker", "kubernetes", "aws", "azure", "jenkins", "git", "linux"]
            }
        }
        
        # Kullanıcı mesajını analiz et
        detected_areas = []
        detected_subtopics = []
        skill_level = "beginner"
        
        # Öğrenme isteği kelimeleri
        learning_request_words = ["öğrenmek", "öğrenmek istiyorum", "öğrenmek istiyor", "öğrenmek istiyoruz", 
                                 "öğrenmek istiyorsun", "öğrenmek istiyorsunuz", "öğrenmek istiyorlar",
                                 "öğrenmek istiyoruz", "öğrenmek istiyoruz", "öğrenmek istiyoruz",
                                 "yol haritası", "roadmap", "nasıl", "hangi", "nereden başlamalı",
                                 "başlamak", "başlamak istiyorum", "başlamak istiyor", "başlamak istiyoruz"]
        
        has_learning_request = any(word in user_message_lower for word in learning_request_words)
        
        for area, config in learning_areas.items():
            for keyword in config["keywords"]:
                if keyword in user_message_lower:
                    detected_areas.append(area)
                    break
            
            for subtopic in config["subtopics"]:
                if subtopic in user_message_lower:
                    detected_subtopics.append(subtopic)
        
        # Seviye belirleme
        if any(word in user_message_lower for word in ["ileri", "advanced", "uzman", "profesyonel"]):
            skill_level = "advanced"
        elif any(word in user_message_lower for word in ["orta", "intermediate", "orta seviye"]):
            skill_level = "intermediate"
        
        # Zaman belirleme
        timeline_months = 6  # varsayılan
        if "hızlı" in user_message_lower or "kısa" in user_message_lower:
            timeline_months = 3
        elif "uzun" in user_message_lower or "detaylı" in user_message_lower:
            timeline_months = 12
        
        # Eğer hiç alan tespit edilmediyse ama öğrenme isteği varsa, genel programlama ekle
        if not detected_areas and has_learning_request:
            detected_areas.append("programlama")
        
        return {
            "learning_areas": list(set(detected_areas)),
            "subtopics": list(set(detected_subtopics)),
            "skill_level": skill_level,
            "timeline_months": timeline_months,
            "has_learning_request": has_learning_request or len(detected_areas) > 0 or len(detected_subtopics) > 0
        }

    def generate_roadmap_suggestion(self, analysis: Dict[str, Any]) -> str:
        """
        AI kullanarak analiz sonuçlarına göre yol haritası önerisi oluşturur
        """
        # API key kontrolü
        if GEMINI_API_KEY == "your_gemini_api_key_here" or not GEMINI_API_KEY:
            return self.get_simple_roadmap_suggestion(analysis)
        
        try:
            suggestion_prompt = f"""
            Aşağıdaki analiz sonuçlarına göre kullanıcıya yol haritası önerisi sun:
            
            Analiz: {json.dumps(analysis, ensure_ascii=False)}
            
            Kullanıcıya şu formatta cevap ver:
            - Öğrenme alanlarını belirt
            - Seviye ve süre bilgisini ver
            - Yol haritası oluşturma önerisi sun
            - Motivasyonel ve destekleyici ol
            
            Maksimum 2-3 cümle, Türkçe.
            """
            
            response = self.model.generate_content(suggestion_prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"AI suggestion error: {e}")
            return self.get_simple_roadmap_suggestion(analysis)

    def get_simple_roadmap_suggestion(self, analysis: Dict[str, Any]) -> str:
        """
        AI çalışmadığında basit kural tabanlı öneri
        """
        if not analysis["has_learning_request"]:
            return "Hangi konuda öğrenmek istediğinizi belirtir misiniz? Size uygun bir yol haritası oluşturabilirim!"
        
        areas = analysis["learning_areas"]
        subtopics = analysis["subtopics"]
        level = analysis["skill_level"]
        timeline = analysis["timeline_months"]
        
        suggestions = []
        
        if "programlama" in areas or any(topic in subtopics for topic in ["python", "javascript", "java"]):
            suggestions.append("programlama temelleri")
        
        if "veri_bilimi" in areas or any(topic in subtopics for topic in ["pandas", "numpy", "matplotlib"]):
            suggestions.append("veri bilimi")
        
        if "web_gelistirme" in areas or any(topic in subtopics for topic in ["html", "css", "javascript", "react"]):
            suggestions.append("web geliştirme")
        
        if "makine_ogrenmesi" in areas or any(topic in subtopics for topic in ["tensorflow", "scikit-learn"]):
            suggestions.append("makine öğrenmesi")
        
        if suggestions:
            suggestion_text = ", ".join(suggestions)
            return f"Harika! {suggestion_text} alanında size özel bir yol haritası oluşturabilirim. {level} seviyede, {timeline} aylık bir plan hazırlayabilirim. Yol haritası oluşturmak ister misiniz?"
        
        return "Bu konuda size yardımcı olabilirim! Daha spesifik bilgi verirseniz size uygun bir yol haritası oluşturabilirim."

    def get_fallback_response(self, user_message: str) -> str:
        """
        AI çalışmadığında dummy cevap döndür
        """
        user_message_lower = user_message.lower()
        
        fallback_responses = {
            "merhaba": "Merhaba! Size nasıl yardımcı olabilirim? MyWisePath'te öğrenme yolculuğunuza başlayabilirsiniz! 🚀",
            "selam": "Selam! Öğrenme tutkunuzu desteklemek için buradayım. Hangi konuda yardıma ihtiyacınız var?",
            "python": "Python harika bir programlama dili! Başlamak için Python.org'daki tutorial'ı öneririm. Ayrıca MyWisePath'te size özel Python yol haritası oluşturabilirim! 🐍",
            "veri bilimi": "Veri bilimi çok heyecan verici bir alan! Python, Pandas, NumPy ve Matplotlib ile başlayabilirsiniz. Size kişiselleştirilmiş bir veri bilimi yol haritası hazırlayabilirim! 📊",
            "web geliştirme": "Web geliştirme için HTML, CSS ve JavaScript temellerini öğrenmeniz gerekiyor. React, Node.js gibi modern teknolojilerle devam edebilirsiniz! 💻",
            "makine öğrenmesi": "Makine öğrenmesi için önce matematik temellerinizi güçlendirmeniz gerekiyor. Python, scikit-learn ve TensorFlow ile başlayabilirsiniz! 🤖",
            "yol haritası": "Size kişiselleştirilmiş bir yol haritası oluşturmak için ilgi alanlarınızı ve hedeflerinizi bilmem gerekiyor. Dashboard'da 'Yol Haritası Oluştur' butonuna tıklayabilirsiniz! 🗺️",
            "javascript": "JavaScript web geliştirmenin temelidir! Modern JavaScript (ES6+) öğrenerek React, Vue.js gibi framework'lerle devam edebilirsiniz! ⚡",
            "react": "React harika bir frontend framework'ü! JavaScript temellerini öğrendikten sonra React ile modern web uygulamaları geliştirebilirsiniz! ⚛️",
            "node.js": "Node.js ile backend geliştirme yapabilirsiniz! JavaScript bilginizi hem frontend hem backend'de kullanabilirsiniz! 🟢",
            "sql": "SQL veritabanı yönetimi için temel dildir! MySQL, PostgreSQL gibi veritabanlarıyla çalışmayı öğrenebilirsiniz! 🗄️",
            "docker": "Docker container teknolojisi ile uygulamalarınızı kolayca deploy edebilirsiniz! DevOps yolculuğunuzda önemli bir adım! 🐳",
            "git": "Git versiyon kontrol sistemi ile kodlarınızı güvenle yönetebilirsiniz! GitHub, GitLab gibi platformlarla işbirliği yapabilirsiniz! 📝",
            "yardım": "Size yardımcı olmaktan mutluluk duyarım! Hangi konuda bilgi almak istiyorsunuz? Programlama, veri bilimi, web geliştirme veya başka bir alan? 🤝",
            "teşekkür": "Rica ederim! Öğrenme yolculuğunuzda size destek olmaya devam edeceğim. Başka sorularınız varsa sormaktan çekinmeyin! 😊"
        }
        
        for keyword, response in fallback_responses.items():
            if keyword in user_message_lower:
                return response
        
        return "Bu konuda size yardımcı olabilirim! Programlama, veri bilimi, web geliştirme gibi alanlarda sorularınızı sorabilirsiniz. Daha spesifik bir soru sorarsanız size daha detaylı bilgi verebilirim! 💡"

# Global AI service instance
ai_service = AIService() 