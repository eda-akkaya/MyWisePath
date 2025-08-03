from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from typing import Dict, Any, List
import random
import asyncio

from models.chatbot import ChatRequest, ChatResponse
from models.roadmap import RoadmapRequest, Roadmap, Module, LearningGoal, SkillAssessment
from utils.auth import verify_token
from services.ai_service import ai_service
from services.educational_content_service import educational_content_service
from services.live_content_service import live_content_service
from config import GEMINI_API_KEY

router = APIRouter(prefix="/api/v1/chatbot", tags=["Chatbot"])
security = HTTPBearer()

# Roadmap templates (roadmap router'ından kopyalandı)
ROADMAP_TEMPLATES = {
    "data_science": {
        "title": "Veri Bilimi Yol Haritası",
        "description": "Sıfırdan veri bilimci olma yolculuğunuz",
        "modules": [
            {
                "id": "ds_1",
                "title": "Python Temelleri",
                "description": "Python programlama dilinin temellerini öğrenin",
                "difficulty": "beginner",
                "estimated_hours": 20,
                "prerequisites": [],
                "resources": ["Python.org Tutorial", "Codecademy Python Course"]
            },
            {
                "id": "ds_2", 
                "title": "Veri Manipülasyonu",
                "description": "Pandas ve NumPy ile veri işleme",
                "difficulty": "beginner",
                "estimated_hours": 25,
                "prerequisites": ["Python Temelleri"],
                "resources": ["Pandas Documentation", "DataCamp Course"]
            },
            {
                "id": "ds_3",
                "title": "Veri Görselleştirme",
                "description": "Matplotlib ve Seaborn ile veri görselleştirme",
                "difficulty": "intermediate",
                "estimated_hours": 15,
                "prerequisites": ["Veri Manipülasyonu"],
                "resources": ["Matplotlib Tutorial", "Seaborn Gallery"]
            },
            {
                "id": "ds_4",
                "title": "Makine Öğrenmesi Temelleri",
                "description": "Scikit-learn ile makine öğrenmesi",
                "difficulty": "intermediate",
                "estimated_hours": 30,
                "prerequisites": ["Veri Görselleştirme"],
                "resources": ["Scikit-learn Documentation", "Coursera ML Course"]
            }
        ]
    },
    "web_development": {
        "title": "Web Geliştirme Yol Haritası",
        "description": "Modern web uygulamaları geliştirme yolculuğu",
        "modules": [
            {
                "id": "web_1",
                "title": "HTML & CSS Temelleri",
                "description": "Web sayfalarının temel yapısını öğrenin",
                "difficulty": "beginner",
                "estimated_hours": 15,
                "prerequisites": [],
                "resources": ["MDN Web Docs", "W3Schools"]
            },
            {
                "id": "web_2",
                "title": "JavaScript Temelleri",
                "description": "Dinamik web uygulamaları için JavaScript",
                "difficulty": "beginner",
                "estimated_hours": 25,
                "prerequisites": ["HTML & CSS Temelleri"],
                "resources": ["JavaScript.info", "Eloquent JavaScript"]
            },
            {
                "id": "web_3",
                "title": "React.js",
                "description": "Modern frontend framework ile uygulama geliştirme",
                "difficulty": "intermediate",
                "estimated_hours": 35,
                "prerequisites": ["JavaScript Temelleri"],
                "resources": ["React Documentation", "React Tutorial"]
            }
        ]
    },
    "python_programming": {
        "title": "Python Programlama Yol Haritası",
        "description": "Python ile programlama öğrenme yolculuğu",
        "modules": [
            {
                "id": "py_1",
                "title": "Python Temelleri",
                "description": "Python syntax ve temel kavramlar",
                "difficulty": "beginner",
                "estimated_hours": 20,
                "prerequisites": [],
                "resources": ["Python.org Tutorial", "freeCodeCamp Python"]
            },
            {
                "id": "py_2",
                "title": "Veri Yapıları ve Algoritmalar",
                "description": "Python'da veri yapıları ve algoritma çözümleri",
                "difficulty": "intermediate",
                "estimated_hours": 30,
                "prerequisites": ["Python Temelleri"],
                "resources": ["Coursera Python Data Structures", "LeetCode Python"]
            },
            {
                "id": "py_3",
                "title": "Web Geliştirme (Django/Flask)",
                "description": "Python ile web uygulamaları geliştirme",
                "difficulty": "intermediate",
                "estimated_hours": 25,
                "prerequisites": ["Veri Yapıları ve Algoritmalar"],
                "resources": ["Django Documentation", "Flask Tutorial"]
            }
        ]
    },
    "machine_learning": {
        "title": "Makine Öğrenmesi Yol Haritası",
        "description": "Makine öğrenmesi ve yapay zeka yolculuğu",
        "modules": [
            {
                "id": "ml_1",
                "title": "Matematik Temelleri",
                "description": "Lineer cebir, kalkülüs ve istatistik",
                "difficulty": "beginner",
                "estimated_hours": 40,
                "prerequisites": [],
                "resources": ["Khan Academy Math", "MIT OpenCourseWare"]
            },
            {
                "id": "ml_2",
                "title": "Python ve Veri Bilimi",
                "description": "Python, Pandas, NumPy ile veri işleme",
                "difficulty": "beginner",
                "estimated_hours": 30,
                "prerequisites": ["Matematik Temelleri"],
                "resources": ["DataCamp Python", "freeCodeCamp Data Analysis"]
            },
            {
                "id": "ml_3",
                "title": "Makine Öğrenmesi Algoritmaları",
                "description": "Scikit-learn ile ML algoritmaları",
                "difficulty": "intermediate",
                "estimated_hours": 35,
                "prerequisites": ["Python ve Veri Bilimi"],
                "resources": ["Coursera ML Course", "Scikit-learn Documentation"]
            },
            {
                "id": "ml_4",
                "title": "Derin Öğrenme",
                "description": "TensorFlow/PyTorch ile neural networks",
                "difficulty": "advanced",
                "estimated_hours": 45,
                "prerequisites": ["Makine Öğrenmesi Algoritmaları"],
                "resources": ["TensorFlow Tutorial", "PyTorch Documentation"]
            }
        ]
    }
}

def get_roadmap_template(interests: list, skill_level: str) -> str:
    """İlgi alanlarına göre uygun roadmap template seç"""
    
    # İlgi alanlarını analiz et
    interests_lower = [interest.lower() for interest in interests]
    
    # Debug için yazdır
    print(f"Chatbot - Interests received: {interests}")
    print(f"Chatbot - Interests lower: {interests_lower}")
    
    # Web Geliştirme kontrolü
    if any(word in interests_lower for word in ["web geliştirme", "web", "frontend", "backend", "html", "css", "javascript"]):
        print("Chatbot - Selected: web_development")
        return "web_development"
    # AI & Machine Learning kontrolü
    elif any(word in interests_lower for word in ["ai & machine learning", "ai", "machine learning", "makine öğrenmesi", "yapay zeka"]):
        print("Chatbot - Selected: machine_learning")
        return "machine_learning"
    # Veri Bilimi kontrolü
    elif any(word in interests_lower for word in ["veri bilimi", "veri", "data", "analiz"]):
        print("Chatbot - Selected: data_science")
        return "data_science"
    # Python kontrolü
    elif any(word in interests_lower for word in ["python", "programlama", "kod"]):
        print("Chatbot - Selected: python_programming")
        return "python_programming"
    else:
        # Varsayılan olarak veri bilimi
        print("Chatbot - Selected: data_science (default)")
        return "data_science"

def create_roadmap_from_template(roadmap_request: RoadmapRequest, user_id: str) -> Roadmap:
    """Template'den roadmap oluştur"""
    
    try:
        # İlgi alanlarına göre roadmap template seç
        roadmap_type = get_roadmap_template(roadmap_request.interests, roadmap_request.skill_level)
        template = ROADMAP_TEMPLATES[roadmap_type]
        
        # Modülleri oluştur
        modules = []
        for i, module_data in enumerate(template["modules"]):
            module = Module(
                id=module_data["id"],
                title=module_data["title"],
                description=module_data["description"],
                difficulty=module_data["difficulty"],
                estimated_hours=module_data["estimated_hours"],
                prerequisites=module_data["prerequisites"],
                resources=module_data["resources"],
                completed=False,
                progress_percentage=0
            )
            modules.append(module)
        
        # Öğrenme hedefleri oluştur
        learning_goals = []
        for goal in roadmap_request.learning_goals:
            learning_goal = LearningGoal(
                title=goal,
                description=f"{goal} alanında uzmanlaşmak",
                target_date=None
            )
            learning_goals.append(learning_goal)
        
        # Beceri değerlendirmeleri oluştur
        skill_assessments = []
        if roadmap_type == "data_science":
            skill_names = ["Python", "Veri Analizi", "Makine Öğrenmesi", "İstatistik"]
        elif roadmap_type == "web_development":
            skill_names = ["HTML/CSS", "JavaScript", "React", "Backend Development"]
        elif roadmap_type == "python_programming":
            skill_names = ["Python", "Algoritma", "Veri Yapıları", "Web Development"]
        elif roadmap_type == "machine_learning":
            skill_names = ["Matematik", "Python", "Makine Öğrenmesi", "Derin Öğrenme"]
        else:
            skill_names = ["Genel Programlama", "Problem Çözme", "Teknoloji"]
        
        for skill in skill_names:
            assessment = SkillAssessment(
                skill_name=skill,
                current_level=roadmap_request.skill_level,
                target_level="advanced",
                progress_percentage=0
            )
            skill_assessments.append(assessment)
        
        # Toplam süre hesapla
        total_hours = sum(module.estimated_hours for module in modules)
        
        # Roadmap oluştur
        roadmap = Roadmap(
            id=f"roadmap_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            title=template["title"],
            description=template["description"],
            created_at=datetime.now(),
            modules=modules,
            learning_goals=learning_goals,
            skill_assessments=skill_assessments,
            total_estimated_hours=total_hours,
            completed_modules=0,
            overall_progress=0
        )
        
        return roadmap
    except Exception as e:
        print(f"Error creating roadmap from template: {e}")
        # Hata durumunda basit bir roadmap oluştur
        fallback_module = Module(
            id="fallback_1",
            title="Temel Programlama",
            description="Programlama temellerini öğrenin",
            difficulty="beginner",
            estimated_hours=20,
            prerequisites=[],
            resources=["Python.org Tutorial", "freeCodeCamp"],
            completed=False,
            progress_percentage=0
        )
        
        fallback_roadmap = Roadmap(
            id=f"roadmap_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            title="Genel Programlama Yol Haritası",
            description="Programlama öğrenme yolculuğunuz",
            created_at=datetime.now(),
            modules=[fallback_module],
            learning_goals=[LearningGoal(title="Programlama öğrenmek", description="Programlama temellerini öğrenmek", target_date=None)],
            skill_assessments=[SkillAssessment(skill_name="Programlama", current_level="beginner", target_level="intermediate", progress_percentage=0)],
            total_estimated_hours=20,
            completed_modules=0,
            overall_progress=0
        )
        
        return fallback_roadmap

async def _enhance_roadmap_with_live_content(template_roadmap: Roadmap, dynamic_roadmap: Dict[str, Any]) -> Roadmap:
    """Template roadmap'i gerçek zamanlı içeriklerle geliştir"""
    try:
        # Dinamik roadmap'ten modülleri al
        dynamic_modules = dynamic_roadmap.get("modules", [])
        
        # Template modüllerini güncelle
        for i, module in enumerate(template_roadmap.modules):
            if i < len(dynamic_modules):
                dynamic_module = dynamic_modules[i]
                
                # Dinamik kaynakları ekle
                live_resources = []
                for resource in dynamic_module.get("resources", []):
                    live_resources.append(f"{resource['title']} ({resource['platform']}) - {resource['url']}")
                
                # Mevcut kaynaklarla birleştir
                module.resources.extend(live_resources)
                
                # Dinamik açıklamayı güncelle
                if dynamic_module.get("description"):
                    module.description = f"{module.description}\n\nGüncel kaynaklar: {dynamic_module['description']}"
        
        # Yeni modüller ekle (eğer dinamik roadmap'te daha fazla modül varsa)
        for i in range(len(template_roadmap.modules), len(dynamic_modules)):
            dynamic_module = dynamic_modules[i]
            
            # Yeni modül oluştur
            new_module = Module(
                id=f"live_{i+1}",
                title=dynamic_module.get("title", f"Modül {i+1}"),
                description=dynamic_module.get("description", ""),
                difficulty=template_roadmap.modules[0].difficulty if template_roadmap.modules else "beginner",
                estimated_hours=10,  # varsayılan
                prerequisites=[],
                resources=[f"{r['title']} ({r['platform']}) - {r['url']}" for r in dynamic_module.get("resources", [])],
                completed=False,
                progress_percentage=0
            )
            
            template_roadmap.modules.append(new_module)
        
        # Toplam süreyi güncelle
        template_roadmap.total_estimated_hours = sum(module.estimated_hours for module in template_roadmap.modules)
        
        return template_roadmap
        
    except Exception as e:
        print(f"Error enhancing roadmap with live content: {e}")
        return template_roadmap

@router.post("/query", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI destekli chatbot ile sohbet et"""
    
    try:
        # Token doğrulama
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        
        # Kullanıcı context'ini oluştur (gelecekte veritabanından alınacak)
        user_context = {
            "user_id": payload.get("sub"),
            "interests": ["programlama", "öğrenme"],
            "skill_level": "beginner"
        }
        
        # Kullanıcı mesajını AI ile analiz et
        analysis = ai_service.analyze_learning_request(request.message)
        
        # Debug için analiz sonucunu yazdır
        print(f"Chatbot Analysis: {analysis}")
        
        # Eğer öğrenme isteği varsa, özel cevap oluştur
        if analysis.get("has_learning_request", False):
            # AI ile yol haritası önerisi oluştur
            roadmap_suggestion = ai_service.generate_roadmap_suggestion(analysis)
            
            # AI ile eğitim içerik önerileri al
            content_recommendations = []
            for area in analysis.get("learning_areas", []):
                recommendations = educational_content_service.get_content_recommendations(
                    area, analysis.get("skill_level", "beginner"), 2
                )
                content_recommendations.extend(recommendations)
            
            # AI ile cevabı oluştur
            response_parts = [roadmap_suggestion]
            
            if content_recommendations:
                response_parts.append("\n\nÖnerilen eğitim kaynakları:")
                for i, rec in enumerate(content_recommendations[:3], 1):
                    response_parts.append(f"{i}. {rec['title']} ({rec['platform']}) - {rec['url']}")
            
            bot_response = "\n".join(response_parts)
        else:
            # AI ile genel cevap al
            bot_response = ai_service.get_ai_response(request.message, user_context)
        
        return ChatResponse(
            message=bot_response,
            timestamp=datetime.now().isoformat(),
            success=True
        )
    except HTTPException:
        # HTTPException'ları tekrar fırlat
        raise
    except Exception as e:
        print(f"Error in chat_with_bot: {e}")
        # Hata durumunda basit bir cevap döndür
        return ChatResponse(
            message="Üzgünüm, şu anda size yardımcı olamıyorum. Lütfen daha sonra tekrar deneyin.",
            timestamp=datetime.now().isoformat(),
            success=False
        )

@router.post("/generate-roadmap")
async def generate_roadmap_from_chat(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI destekli chatbot mesajından yol haritası oluştur"""
    
    try:
        # Token doğrulama
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        
        # Kullanıcı mesajını AI ile analiz et
        analysis = ai_service.analyze_learning_request(request.message)
        
        # Eğer öğrenme isteği yoksa, varsayılan değerler kullan
        if not analysis.get("has_learning_request", False):
            analysis["has_learning_request"] = True
            analysis["learning_areas"] = ["programlama"]
            analysis["skill_level"] = "beginner"
            analysis["timeline_months"] = 6
        
        # Gerçek zamanlı içerik araştırması yap
        topic = analysis.get("learning_areas", ["programlama"])[0]
        skill_level = analysis.get("skill_level", "beginner")
        
        # Kullanıcı tercihleri
        user_preferences = {
            "skill_level": skill_level,
            "learning_style": "practical",  # pratik odaklı
            "preferred_platforms": ["coursera", "udemy", "freecodecamp", "youtube"],
            "time_commitment": "10 hours per week",
            "budget": "free_and_paid"
        }
        
        # Dinamik roadmap oluştur
        dynamic_roadmap = await live_content_service.create_dynamic_roadmap(
            topic, skill_level, user_preferences
        )
        
        # Template roadmap ile birleştir
        template_roadmap = create_roadmap_from_template(
            RoadmapRequest(
                skill_level=skill_level,
                interests=analysis.get("learning_areas", []) + analysis.get("subtopics", []),
                learning_goals=[f"{area} öğrenmek" for area in analysis.get("learning_areas", [])],
                available_hours_per_week=10,
                target_timeline_months=analysis.get("timeline_months", 6)
            ),
            payload.get("sub")
        )
        
        # Dinamik içerikleri template'e ekle
        enhanced_roadmap = await _enhance_roadmap_with_live_content(template_roadmap, dynamic_roadmap)
        
        return {
            "roadmap": enhanced_roadmap,
            "analysis": analysis,
            "live_content": dynamic_roadmap,
            "message": f"'{request.message}' isteğinize göre güncel eğitim kaynaklarıyla {len(enhanced_roadmap.modules)} modüllük bir yol haritası oluşturdum!",
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
    except HTTPException:
        # HTTPException'ları tekrar fırlat
        raise
    except Exception as e:
        print(f"Error generating roadmap from chat: {e}")
        # Hata durumunda basit bir roadmap oluştur
        try:
            fallback_request = RoadmapRequest(
                skill_level="beginner",
                interests=["programlama"],
                learning_goals=["Programlama öğrenmek"],
                available_hours_per_week=10,
                target_timeline_months=6
            )
            fallback_roadmap = create_roadmap_from_template(fallback_request, "fallback_user")
            
            return {
                "roadmap": fallback_roadmap,
                "analysis": {"has_learning_request": True, "learning_areas": ["programlama"]},
                "message": "Genel bir programlama yol haritası oluşturdum!",
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
        except Exception as fallback_error:
            print(f"Fallback roadmap creation error: {fallback_error}")
            raise HTTPException(status_code=500, detail="Yol haritası oluşturulurken bir hata oluştu")

@router.get("/content-recommendations/{topic}")
async def get_content_recommendations(
    topic: str,
    skill_level: str = "beginner",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI ile belirli bir konu için eğitim içerik önerileri getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        recommendations = educational_content_service.get_content_recommendations(
            topic, skill_level, 10
        )
        
        return {
            "topic": topic,
            "skill_level": skill_level,
            "recommendations": recommendations,
            "total_count": len(recommendations),
            "timestamp": datetime.now().isoformat(),
            "ai_generated": True
        }
    except Exception as e:
        print(f"Error getting content recommendations: {e}")
        raise HTTPException(status_code=500, detail="Eğitim önerileri alınırken hata oluştu")

@router.post("/search-education")
async def search_education_content(
    query: str,
    skill_level: str = "beginner",
    limit: int = 5,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI ile eğitim içeriği ara"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        results = educational_content_service.search_content(query, skill_level, limit)
        
        return {
            "query": query,
            "skill_level": skill_level,
            "results": results,
            "total_count": len(results),
            "timestamp": datetime.now().isoformat(),
            "ai_generated": True
        }
    except Exception as e:
        print(f"Error searching education content: {e}")
        raise HTTPException(status_code=500, detail="Eğitim araması yapılırken hata oluştu")

@router.get("/popular-education")
async def get_popular_education(
    limit: int = 5,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """AI ile popüler eğitim içeriklerini getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        popular_content = educational_content_service.get_popular_content(limit)
        
        return {
            "popular_content": popular_content,
            "total_count": len(popular_content),
            "timestamp": datetime.now().isoformat(),
            "ai_generated": True
        }
    except Exception as e:
        print(f"Error getting popular education: {e}")
        raise HTTPException(status_code=500, detail="Popüler eğitimler alınırken hata oluştu")

@router.get("/welcome")
async def get_welcome_message():
    """AI destekli karşılama mesajını getir"""
    try:
        # AI ile karşılama mesajı oluştur
        welcome_prompt = """
        Sen MyWisePath öğrenme platformunun AI asistanısın. 
        Kullanıcıya kısa, samimi ve motivasyonel bir karşılama mesajı ver.
        Öğrenme yolculuğunda yardımcı olacağını belirt.
        Maksimum 2 cümle, Türkçe.
        """
        
        response = ai_service.model.generate_content(welcome_prompt)
        message = response.text.strip()
        
        return {
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"AI welcome message error: {e}")
        # Fallback mesaj
        return {
            "message": "Merhaba öğrenme tutkusu hiç bitmeyen insan! Ne öğrenmek istersin?",
            "timestamp": datetime.now().isoformat()
        } 

@router.get("/debug/test")
async def debug_test():
    """Debug test endpoint"""
    return {
        "message": "Chatbot router çalışıyor!",
        "timestamp": datetime.now().isoformat(),
        "ai_service_available": True,
        "educational_content_available": True,
        "gemini_api_key_set": bool(GEMINI_API_KEY)
    }

@router.post("/search-live-content")
async def search_live_content(
    topic: str,
    skill_level: str = "beginner",
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Gerçek zamanlı internet araştırması yaparak eğitim içerikleri bul"""
    
    try:
        # Token doğrulama
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        
        # Gerçek zamanlı içerik ara
        live_content = await live_content_service.search_live_content(topic, skill_level, limit)
        
        return {
            "topic": topic,
            "skill_level": skill_level,
            "content": live_content,
            "total_count": len(live_content),
            "timestamp": datetime.now().isoformat(),
            "live_search": True
        }
        
    except Exception as e:
        print(f"Live content search error: {e}")
        raise HTTPException(status_code=500, detail="İçerik arama sırasında hata oluştu")

@router.post("/create-dynamic-roadmap")
async def create_dynamic_roadmap(
    topic: str,
    skill_level: str = "beginner",
    user_preferences: dict = None,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Gerçek zamanlı araştırma ile dinamik roadmap oluştur"""
    
    try:
        # Token doğrulama
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        
        # Varsayılan tercihler
        if user_preferences is None:
            user_preferences = {
                "skill_level": skill_level,
                "learning_style": "practical",
                "preferred_platforms": ["coursera", "udemy", "freecodecamp", "youtube"],
                "time_commitment": "10 hours per week",
                "budget": "free_and_paid"
            }
        
        # Dinamik roadmap oluştur
        dynamic_roadmap = await live_content_service.create_dynamic_roadmap(
            topic, skill_level, user_preferences
        )
        
        return {
            "topic": topic,
            "skill_level": skill_level,
            "roadmap": dynamic_roadmap,
            "user_preferences": user_preferences,
            "timestamp": datetime.now().isoformat(),
            "live_generated": True
        }
        
    except Exception as e:
        print(f"Dynamic roadmap creation error: {e}")
        raise HTTPException(status_code=500, detail="Dinamik roadmap oluşturulurken hata oluştu") 