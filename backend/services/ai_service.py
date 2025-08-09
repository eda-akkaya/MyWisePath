import google.generativeai as genai
from typing import Optional, Dict, List, Any
from config import GEMINI_API_KEY
import json
import re
from services.serp_ai_service import serp_ai_service

# Gemini API'yi yapılandır
genai.configure(api_key=GEMINI_API_KEY)

class AIService:
    def __init__(self):
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Gemini model'ini başlat"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            print("Gemini model başarıyla başlatıldı")
        except Exception as e:
            print(f"Gemini model başlatma hatası: {e}")
            self.model = None

    def get_ai_response(self, user_message: str, user_context: Optional[dict] = None, user_profile: Optional[dict] = None, roadmap_info: Optional[dict] = None) -> str:
        """
        AI ile kullanıcı mesajına cevap ver
        
        Args:
            user_message: Kullanıcı mesajı
            user_context: Kullanıcı context'i (eski parametre)
            user_profile: Kullanıcı profil bilgileri (eski parametre)
            roadmap_info: Roadmap oluşturma sırasındaki kullanıcı bilgileri (yeni parametre)
        """
        
        try:
            # Dinamik sistem prompt'u oluştur - roadmap bilgileri öncelikli
            if roadmap_info:
                system_prompt = self._generate_roadmap_based_system_prompt(roadmap_info)
            else:
                system_prompt = self._generate_dynamic_system_prompt(user_profile)
            
            # Kullanıcı context'ini formatla (geriye uyumluluk için)
            context_str = ""
            if user_context:
                context_str = f"Kullanıcı bilgileri: {user_context}"
            
            # Profil bilgilerini ekle
            if user_profile:
                profile_info = self._format_user_profile(user_profile)
                context_str += f"\n{profile_info}"
            
            system_prompt = system_prompt.format(user_context=context_str)
            
            # Gemini API'ye istek gönder
            prompt = f"{system_prompt}\n\nKullanıcı: {user_message}\n\nAsistan:"
            response = self.model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini API Error: {e}")
            # Fallback cevap
            return self.get_fallback_response(user_message)

    def _generate_dynamic_system_prompt(self, user_profile: Optional[dict] = None) -> str:
        """
        Kullanıcı profil bilgilerine göre dinamik sistem prompt'u oluştur
        """
        base_prompt = """Sen MyWisePath öğrenme platformunun Bilge Rehber ✨'sin. 
        Kullanıcılara öğrenme yolculuklarında yardımcı oluyorsun.
        
        Özelliklerin:
        - Öğrenme konularında rehberlik etme
        - Yol haritası önerileri sunma
        - Programlama, veri bilimi, web geliştirme konularında bilgi verme
        - Motivasyonel ve destekleyici olma
        - Türkçe cevap verme
        - Kullanıcı isteklerini analiz edip uygun öğrenme alanlarını belirleme"""
        
        if not user_profile:
            return base_prompt + """
            
            Kullanıcı profil bilgileri: {user_context}
            
            Eğer kullanıcı bir konu öğrenmek istiyorsa, o konuyla ilgili detaylı bilgi ver ve yol haritası oluşturma önerisi sun.
            Kısa, net ve yardımcı cevaplar ver. Maksimum 3-4 cümle."""
        
        # Kullanıcı seviyesine göre prompt ayarla
        skill_level = user_profile.get('skill_level', 'beginner')
        interests = user_profile.get('interests', [])
        learning_goals = user_profile.get('learning_goals', [])
        
        # Seviyeye göre özel talimatlar
        level_instructions = self._get_level_specific_instructions(skill_level)
        
        # İlgi alanlarına göre özel talimatlar
        interest_instructions = self._get_interest_specific_instructions(interests)
        
        # Öğrenme hedeflerine göre özel talimatlar
        goal_instructions = self._get_goal_specific_instructions(learning_goals)
        
        dynamic_prompt = base_prompt + f"""
        
        {level_instructions}
        {interest_instructions}
        {goal_instructions}
        
        Kullanıcı profil bilgileri: {{user_context}}
        
        Bu kullanıcının seviyesi: {skill_level}
        İlgi alanları: {', '.join(interests) if interests else 'Belirtilmemiş'}
        Öğrenme hedefleri: {', '.join(learning_goals) if learning_goals else 'Belirtilmemiş'}
        
        Kullanıcının seviyesine ve ilgi alanlarına uygun, kişiselleştirilmiş cevaplar ver.
        Eğer kullanıcı bir konu öğrenmek istiyorsa, seviyesine uygun detaylı bilgi ver ve yol haritası oluşturma önerisi sun.
        Kısa, net ve yardımcı cevaplar ver. Maksimum 3-4 cümle."""
        
        return dynamic_prompt

    def _generate_roadmap_based_system_prompt(self, roadmap_info: dict) -> str:
        """
        Roadmap oluşturma sırasındaki kullanıcı bilgilerine göre dinamik sistem prompt'u oluştur
        """
        base_prompt = """Sen MyWisePath öğrenme platformunun Bilge Rehber ✨'sin. 
        Kullanıcılara öğrenme yolculuklarında yardımcı oluyorsun.
        
        Özelliklerin:
        - Öğrenme konularında rehberlik etme
        - Yol haritası önerileri sunma
        - Programlama, veri bilimi, web geliştirme konularında bilgi verme
        - Motivasyonel ve destekleyici olma
        - Türkçe cevap verme
        - Kullanıcı isteklerini analiz edip uygun öğrenme alanlarını belirleme"""
        
        # Roadmap bilgilerini al
        skill_level = roadmap_info.get('skill_level', 'beginner')
        interests = roadmap_info.get('interests', [])
        learning_goals = roadmap_info.get('learning_goals', [])
        available_hours = roadmap_info.get('available_hours_per_week', 10)
        timeline_months = roadmap_info.get('target_timeline_months', 6)
        
        # Seviyeye göre özel talimatlar
        level_instructions = self._get_level_specific_instructions(skill_level)
        
        # İlgi alanlarına göre özel talimatlar
        interest_instructions = self._get_interest_specific_instructions(interests)
        
        # Öğrenme hedeflerine göre özel talimatlar
        goal_instructions = self._get_goal_specific_instructions(learning_goals)
        
        # Zaman planına göre özel talimatlar
        time_instructions = self._get_time_based_instructions(available_hours, timeline_months)
        
        dynamic_prompt = base_prompt + f"""
        
        {level_instructions}
        {interest_instructions}
        {goal_instructions}
        {time_instructions}
        
        Kullanıcı profil bilgileri: {{user_context}}
        
        Bu kullanıcının seviyesi: {skill_level}
        İlgi alanları: {', '.join(interests) if interests else 'Belirtilmemiş'}
        Öğrenme hedefleri: {', '.join(learning_goals) if learning_goals else 'Belirtilmemiş'}
        Haftalık çalışma süresi: {available_hours} saat
        Hedef süre: {timeline_months} ay
        
        Kullanıcının seviyesine, ilgi alanlarına ve zaman planına uygun, kişiselleştirilmiş cevaplar ver.
        Eğer kullanıcı bir konu öğrenmek istiyorsa, seviyesine ve zaman planına uygun detaylı bilgi ver ve yol haritası oluşturma önerisi sun.
        Kısa, net ve yardımcı cevaplar ver. Maksimum 3-4 cümle."""
        
        return dynamic_prompt

    def _get_level_specific_instructions(self, skill_level: str) -> str:
        """Seviyeye göre özel talimatlar"""
        instructions = {
            'beginner': """
            - Temel kavramları açık ve basit şekilde açıkla
            - Jargon kullanmaktan kaçın
            - Adım adım rehberlik et
            - Motivasyonel ol ve cesaretlendir
            - Başlangıç kaynakları öner
            """,
            'intermediate': """
            - Orta seviye kavramları detaylandır
            - Pratik örnekler ver
            - İleri seviye kaynaklara yönlendir
            - Proje tabanlı öğrenme öner
            - Best practice'leri vurgula
            """,
            'advanced': """
            - İleri seviye konulara odaklan
            - Karmaşık kavramları açıkla
            - Uzman seviyesi kaynaklar öner
            - Performans optimizasyonu konularına değin
            - Güncel trendleri ve teknolojileri paylaş
            """
        }
        return instructions.get(skill_level, instructions['beginner'])

    def _get_interest_specific_instructions(self, interests: list) -> str:
        """İlgi alanlarına göre özel talimatlar"""
        if not interests:
            return ""
        
        instructions = []
        interests_lower = [interest.lower() for interest in interests]
        
        if any(word in interests_lower for word in ['ai', 'yapay zeka', 'machine learning', 'makine öğrenmesi']):
            instructions.append("- AI ve ML konularında güncel bilgiler paylaş")
            instructions.append("- TensorFlow, PyTorch gibi framework'ler hakkında bilgi ver")
        
        if any(word in interests_lower for word in ['web', 'frontend', 'backend', 'javascript', 'react']):
            instructions.append("- Web geliştirme konularında pratik öneriler sun")
            instructions.append("- Modern web teknolojileri hakkında bilgi ver")
        
        if any(word in interests_lower for word in ['python', 'programlama']):
            instructions.append("- Python programlama konularında detaylı rehberlik et")
            instructions.append("- Python ekosistemi ve kütüphaneler hakkında bilgi ver")
        
        if any(word in interests_lower for word in ['veri', 'data', 'analiz']):
            instructions.append("- Veri analizi ve görselleştirme konularında yardım et")
            instructions.append("- Pandas, NumPy, Matplotlib gibi kütüphaneler hakkında bilgi ver")
        
        return "\n".join(instructions) if instructions else ""

    def _get_goal_specific_instructions(self, learning_goals: list) -> str:
        """Öğrenme hedeflerine göre özel talimatlar"""
        if not learning_goals:
            return ""
        
        instructions = []
        
        for goal in learning_goals:
            goal_lower = goal.lower()
            if 'kariyer' in goal_lower or 'iş' in goal_lower:
                instructions.append("- Kariyer odaklı öneriler sun")
                instructions.append("- Endüstri trendlerini paylaş")
            elif 'proje' in goal_lower:
                instructions.append("- Proje tabanlı öğrenme öner")
                instructions.append("- Portfolio geliştirme konularında yardım et")
            elif 'sertifika' in goal_lower or 'sınav' in goal_lower:
                instructions.append("- Sertifika programları hakkında bilgi ver")
                instructions.append("- Sınav hazırlık stratejileri öner")
        
        return "\n".join(instructions) if instructions else ""

    def _get_time_based_instructions(self, available_hours: int, timeline_months: int) -> str:
        """Zaman planına göre özel talimatlar"""
        instructions = []
        
        # Haftalık çalışma süresine göre
        if available_hours <= 5:
            instructions.append("- Yoğun programlar yerine esnek öğrenme yöntemleri öner")
            instructions.append("- Kısa ve etkili öğrenme teknikleri paylaş")
        elif available_hours <= 15:
            instructions.append("- Dengeli bir öğrenme programı öner")
            instructions.append("- Pratik projeler ve teorik bilgiyi dengeleyen yaklaşımlar sun")
        else:
            instructions.append("- Yoğun ve hızlı ilerleme odaklı programlar öner")
            instructions.append("- İleri seviye projeler ve derinlemesine öğrenme teknikleri paylaş")
        
        # Hedef süreye göre
        if timeline_months <= 3:
            instructions.append("- Hızlı öğrenme stratejileri ve yoğun programlar öner")
            instructions.append("- Odaklanmış ve hedefe yönelik yaklaşımlar sun")
        elif timeline_months <= 6:
            instructions.append("- Dengeli ve sürdürülebilir öğrenme planları öner")
            instructions.append("- Adım adım ilerleme stratejileri paylaş")
        else:
            instructions.append("- Uzun vadeli ve kapsamlı öğrenme programları öner")
            instructions.append("- Derinlemesine uzmanlaşma fırsatları sun")
        
        return "\n".join(instructions) if instructions else ""

    def _format_user_profile(self, user_profile: dict) -> str:
        """Kullanıcı profil bilgilerini formatla"""
        profile_parts = []
        
        if user_profile.get('skill_level'):
            profile_parts.append(f"Seviye: {user_profile['skill_level']}")
        
        if user_profile.get('interests'):
            profile_parts.append(f"İlgi alanları: {', '.join(user_profile['interests'])}")
        
        if user_profile.get('learning_goals'):
            profile_parts.append(f"Öğrenme hedefleri: {', '.join(user_profile['learning_goals'])}")
        
        return " | ".join(profile_parts) if profile_parts else ""

    async def get_ai_response_with_serp_search(self, user_message: str, user_context: Optional[dict] = None, user_profile: Optional[dict] = None, roadmap_info: Optional[dict] = None) -> Dict[str, Any]:
        """
        Serp AI ile entegre AI cevabı döndür
        
        Args:
            user_message: Kullanıcı mesajı
            user_context: Kullanıcı context'i
            user_profile: Kullanıcı profil bilgileri (eski parametre)
            roadmap_info: Roadmap oluşturma sırasındaki kullanıcı bilgileri (yeni parametre)
        """
        try:
            # Kullanıcı mesajından öğrenme kavramlarını çıkar
            learning_concepts = serp_ai_service.extract_learning_concepts(user_message)
            
            # AI ile temel cevap al - roadmap bilgilerini geç
            base_response = self.get_ai_response(user_message, user_context, user_profile, roadmap_info)
            
            # Eğer öğrenme kavramları bulunduysa, Serp AI ile arama yap
            serp_results = []
            if learning_concepts:
                # Kullanıcı seviyesini al - roadmap bilgileri öncelikli
                skill_level = None
                if roadmap_info:
                    skill_level = roadmap_info.get('skill_level', 'beginner')
                elif user_profile:
                    skill_level = user_profile.get('skill_level', 'beginner')
                else:
                    skill_level = 'beginner'
                
                for concept in learning_concepts[:3]:  # En fazla 3 kavram
                    results = await serp_ai_service.search_educational_content(concept, skill_level, 3)
                    serp_results.extend(results)
            
            return {
                "message": base_response,
                "learning_concepts": learning_concepts,
                "serp_results": serp_results,
                "has_educational_content": len(serp_results) > 0
            }
            
        except Exception as e:
            print(f"AI with Serp search error: {e}")
            return {
                "message": self.get_fallback_response(user_message),
                "learning_concepts": [],
                "serp_results": [],
                "has_educational_content": False
            }

    def analyze_learning_request(self, user_message: str) -> Dict[str, Any]:
        """
        AI kullanarak kullanıcı mesajını analiz ederek öğrenme isteğini çıkarır
        """
        # API key kontrolü
        if not GEMINI_API_KEY:
            print("Gemini API key ayarlanmamış, basit analiz döndürülüyor")
            return self.get_simple_analysis(user_message)
        
        try:
            # AI analiz prompt'u
            analysis_prompt = f"""
            Aşağıdaki kullanıcı mesajını analiz et ve JSON formatında cevap ver:
            
            Kullanıcı mesajı: \"{user_message}\"
            
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
                    json_str = json_match.group(0)
                    return json.loads(json_str)
                else:
                    return self.get_simple_analysis(user_message)
            except Exception as e:
                print(f"JSON parse error: {e}")
                return self.get_simple_analysis(user_message)
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return self.get_simple_analysis(user_message)

    async def analyze_learning_request_with_serp(self, user_message: str) -> Dict[str, Any]:
        """
        Serp AI ile entegre öğrenme isteği analizi
        """
        try:
            # Temel analiz
            base_analysis = self.analyze_learning_request(user_message)
            
            # Serp AI ile kavram çıkarma
            learning_concepts = serp_ai_service.extract_learning_concepts(user_message)
            
            # Serp AI ile eğitim içeriği arama
            serp_results = []
            if learning_concepts:
                for concept in learning_concepts[:3]:
                    results = await serp_ai_service.search_educational_content(concept, base_analysis.get("skill_level", "beginner"), 2)
                    serp_results.extend(results)
            
            # Analizi genişlet
            enhanced_analysis = {
                **base_analysis,
                "extracted_concepts": learning_concepts,
                "serp_results": serp_results,
                "has_serp_content": len(serp_results) > 0
            }
            
            return enhanced_analysis
            
        except Exception as e:
            print(f"Enhanced analysis error: {e}")
            return self.analyze_learning_request(user_message)

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
        if not GEMINI_API_KEY:
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