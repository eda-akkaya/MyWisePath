from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from typing import List
import random
import json

from models.roadmap import Roadmap, RoadmapRequest, Module, LearningGoal, SkillAssessment
from utils.auth import verify_token
from services.ai_service import ai_service
from services.educational_content_service import educational_content_service

router = APIRouter(prefix="/api/v1/roadmap", tags=["Roadmap"])
security = HTTPBearer()

def generate_ai_roadmap(interests: List[str], skill_level: str, learning_goals: List[str]) -> dict:
    """AI kullanarak dinamik roadmap oluştur"""
    
    # API key kontrolü
    from config import GEMINI_API_KEY
    if not GEMINI_API_KEY:
        print("Gemini API key ayarlanmamış, fallback roadmap döndürülüyor")
        return get_fallback_roadmap(interests, skill_level)
    
    try:
        # AI ile roadmap oluştur
        prompt = f"""
        Aşağıdaki kullanıcı bilgilerine göre kişiselleştirilmiş bir öğrenme yol haritası oluştur:
        
        İlgi Alanları: {', '.join(interests)}
        Seviye: {skill_level}
        Öğrenme Hedefleri: {', '.join(learning_goals)}
        
        Yol haritası için şu bilgileri JSON formatında ver:
        - title: Yol haritası başlığı
        - description: Yol haritası açıklaması
        - modules: Modüller listesi (her modül için id, title, description, difficulty, estimated_hours, prerequisites, resources)
        
        Modüller şu formatta olmalı:
        [
            {{
                "id": "unique_id",
                "title": "Modül Başlığı",
                "description": "Modül açıklaması",
                "difficulty": "beginner/intermediate/advanced",
                "estimated_hours": sayı,
                "prerequisites": ["ön koşul1", "ön koşul2"],
                "resources": ["kaynak1", "kaynak2"]
            }}
        ]
        
        Sadece JSON formatında cevap ver, başka açıklama ekleme.
        """
        
        if not ai_service.model:
            print("AI model mevcut değil, fallback roadmap kullanılıyor")
            return get_fallback_roadmap(interests, skill_level)
            
        try:
            response = ai_service.model.generate_content(prompt)
            response_text = response.text.strip()
        except Exception as e:
            print(f"AI model error: {e}")
            return get_fallback_roadmap(interests, skill_level)
        
        print(f"AI Response: {response_text}")
        
        # JSON'u parse et
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                roadmap_data = json.loads(json_match.group())
                # Gerekli alanları kontrol et
                if "title" not in roadmap_data or "description" not in roadmap_data or "modules" not in roadmap_data:
                    print("JSON'da gerekli alanlar eksik, fallback kullanılıyor")
                    return get_fallback_roadmap(interests, skill_level)
                return roadmap_data
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                return get_fallback_roadmap(interests, skill_level)
        else:
            print("JSON bulunamadı, fallback kullanılıyor")
            return get_fallback_roadmap(interests, skill_level)
            
    except Exception as e:
        print(f"AI roadmap generation error: {e}")
        # Fallback olarak basit roadmap döndür
        return get_fallback_roadmap(interests, skill_level)

def get_resource_urls():
    """Eğitim kaynaklarının URL'lerini döndür"""
    return {
        # Python Resources
        "Python.org Tutorial": "https://docs.python.org/3/tutorial/",
        "freeCodeCamp Python": "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
        "Codecademy Python": "https://www.codecademy.com/learn/learn-python-3",
        "Coursera Python Data Structures": "https://www.coursera.org/learn/python-data",
        "LeetCode Python": "https://leetcode.com/problemset/all/?languageTags=python",
        "HackerRank Python": "https://www.hackerrank.com/domains/python",
        "Django Documentation": "https://docs.djangoproject.com/",
        "Flask Tutorial": "https://flask.palletsprojects.com/en/2.3.x/quickstart/",
        "Real Python Web Dev": "https://realpython.com/tutorials/web-dev/",
        
        # Web Development Resources
        "MDN Web Docs": "https://developer.mozilla.org/en-US/docs/Web",
        "W3Schools": "https://www.w3schools.com/",
        "freeCodeCamp HTML/CSS": "https://www.freecodecamp.org/learn/responsive-web-design/",
        "JavaScript.info": "https://javascript.info/",
        "Eloquent JavaScript": "https://eloquentjavascript.net/",
        "freeCodeCamp JavaScript": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
        "React Documentation": "https://react.dev/",
        "React Tutorial": "https://react.dev/learn",
        "Udemy React Course": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
        "Node.js Documentation": "https://nodejs.org/en/docs/",
        "Express.js Tutorial": "https://expressjs.com/",
        "freeCodeCamp Backend": "https://www.freecodecamp.org/learn/back-end-development-and-apis/",
        
        # Data Science Resources
        "Codecademy Python Course": "https://www.codecademy.com/learn/learn-python-3",
        "Pandas Documentation": "https://pandas.pydata.org/docs/",
        "NumPy Documentation": "https://numpy.org/doc/",
        "Matplotlib Tutorial": "https://matplotlib.org/stable/tutorials/index.html",
        "Seaborn Tutorial": "https://seaborn.pydata.org/tutorial.html",
        "scikit-learn Tutorial": "https://scikit-learn.org/stable/tutorial/",
        "Kaggle Courses": "https://www.kaggle.com/learn",
        "DataCamp Python": "https://www.datacamp.com/courses/intro-to-python-for-data-science",
        
        # Machine Learning Resources
        "TensorFlow Tutorial": "https://www.tensorflow.org/tutorials",
        "PyTorch Tutorial": "https://pytorch.org/tutorials/",
        "Andrew Ng ML Course": "https://www.coursera.org/learn/machine-learning",
        "fast.ai": "https://www.fast.ai/",
        "Stanford CS231n": "http://cs231n.stanford.edu/",
        "Stanford CS224N": "http://web.stanford.edu/class/cs224n/",
        "OpenCV": "https://opencv.org/",
        "NLTK": "https://www.nltk.org/",
        "spaCy": "https://spacy.io/",
        
        # Cloud & DevOps
        "AWS Machine Learning": "https://aws.amazon.com/machine-learning/",
        "Google Cloud AI": "https://cloud.google.com/ai",
        "Azure Machine Learning": "https://azure.microsoft.com/en-us/services/machine-learning/",
        "Docker Tutorial": "https://docs.docker.com/get-started/",
        "Kubernetes Tutorial": "https://kubernetes.io/docs/tutorials/",
        "Git Tutorial": "https://git-scm.com/doc",
        "GitHub Learning": "https://docs.github.com/en/get-started"
    }

def get_fallback_roadmap(interests: List[str], skill_level: str) -> dict:
    """AI çalışmadığında basit roadmap döndür"""
    
    import random
    
    # Resource URL'lerini al
    resource_urls = get_resource_urls()
    
    # İlgi alanlarına göre basit roadmap oluştur
    interests_text = ' '.join(interests).lower()
    
    # Python roadmap
    if any(word in interests_text for word in ["python", "programlama", "kod"]):
        python_modules = [
            {
                "id": "py_1",
                "title": "Python Temelleri",
                "description": "Python syntax ve temel kavramlar",
                "difficulty": "beginner",
                "estimated_hours": 20,
                "prerequisites": [],
                "resources": [
                    "Python.org Tutorial: " + resource_urls.get("Python.org Tutorial", "#"),
                    "freeCodeCamp Python: " + resource_urls.get("freeCodeCamp Python", "#"),
                    "Codecademy Python: " + resource_urls.get("Codecademy Python", "#")
                ]
            },
            {
                "id": "py_2",
                "title": "Veri Yapıları ve Algoritmalar",
                "description": "Python'da veri yapıları ve algoritma çözümleri",
                "difficulty": "intermediate",
                "estimated_hours": 30,
                "prerequisites": ["Python Temelleri"],
                "resources": [
                    "Coursera Python Data Structures: " + resource_urls.get("Coursera Python Data Structures", "#"),
                    "LeetCode Python: " + resource_urls.get("LeetCode Python", "#"),
                    "HackerRank Python: " + resource_urls.get("HackerRank Python", "#")
                ]
            },
            {
                "id": "py_3",
                "title": "Web Geliştirme (Django/Flask)",
                "description": "Python ile web uygulamaları geliştirme",
                "difficulty": "intermediate",
                "estimated_hours": 25,
                "prerequisites": ["Veri Yapıları ve Algoritmalar"],
                "resources": [
                    "Django Documentation: " + resource_urls.get("Django Documentation", "#"),
                    "Flask Tutorial: " + resource_urls.get("Flask Tutorial", "#"),
                    "Real Python Web Dev: " + resource_urls.get("Real Python Web Dev", "#")
                ]
            }
        ]
        
        return {
            "title": "Python Programlama Yol Haritası",
            "description": "Python ile programlama öğrenme yolculuğu",
            "modules": random.sample(python_modules, min(3, len(python_modules)))
        }
    
    # Web Development roadmap
    elif any(word in interests_text for word in ["web", "frontend", "backend", "html", "css", "javascript"]):
        web_modules = [
            {
                "id": "web_1",
                "title": "HTML & CSS Temelleri",
                "description": "Web sayfalarının temel yapısını öğrenin",
                "difficulty": "beginner",
                "estimated_hours": 15,
                "prerequisites": [],
                "resources": [
                    "MDN Web Docs: " + resource_urls.get("MDN Web Docs", "#"),
                    "W3Schools: " + resource_urls.get("W3Schools", "#"),
                    "freeCodeCamp HTML/CSS: " + resource_urls.get("freeCodeCamp HTML/CSS", "#")
                ]
            },
            {
                "id": "web_2",
                "title": "JavaScript Temelleri",
                "description": "Dinamik web uygulamaları için JavaScript",
                "difficulty": "beginner",
                "estimated_hours": 25,
                "prerequisites": ["HTML & CSS Temelleri"],
                "resources": [
                    "JavaScript.info: " + resource_urls.get("JavaScript.info", "#"),
                    "Eloquent JavaScript: " + resource_urls.get("Eloquent JavaScript", "#"),
                    "freeCodeCamp JavaScript: " + resource_urls.get("freeCodeCamp JavaScript", "#")
                ]
            },
            {
                "id": "web_3",
                "title": "React.js Framework",
                "description": "Modern frontend framework ile uygulama geliştirme",
                "difficulty": "intermediate",
                "estimated_hours": 35,
                "prerequisites": ["JavaScript Temelleri"],
                "resources": [
                    "React Documentation: " + resource_urls.get("React Documentation", "#"),
                    "React Tutorial: " + resource_urls.get("React Tutorial", "#"),
                    "Udemy React Course: " + resource_urls.get("Udemy React Course", "#")
                ]
            },
            {
                "id": "web_4",
                "title": "Node.js Backend",
                "description": "JavaScript ile backend geliştirme",
                "difficulty": "intermediate",
                "estimated_hours": 30,
                "prerequisites": ["JavaScript Temelleri"],
                "resources": [
                    {"name": "Node.js Documentation", "url": resource_urls.get("Node.js Documentation", "#")},
                    {"name": "Express.js Tutorial", "url": resource_urls.get("Express.js Tutorial", "#")},
                    {"name": "freeCodeCamp Backend", "url": resource_urls.get("freeCodeCamp Backend", "#")}
                ]
            }
        ]
        
        return {
            "title": "Web Geliştirme Yol Haritası",
            "description": "Modern web uygulamaları geliştirme yolculuğu",
            "modules": random.sample(web_modules, min(4, len(web_modules)))
        }
    
    # Data Science roadmap
    elif any(word in interests_text for word in ["veri", "data", "analiz", "pandas", "numpy"]):
        data_modules = [
            {
                "id": "ds_1",
                "title": "Python Temelleri",
                "description": "Python programlama dilinin temellerini öğrenin",
                "difficulty": "beginner",
                "estimated_hours": 20,
                "prerequisites": [],
                "resources": [
                    {"name": "Python.org Tutorial", "url": resource_urls.get("Python.org Tutorial", "#")},
                    {"name": "Codecademy Python Course", "url": resource_urls.get("Codecademy Python Course", "#")},
                    {"name": "freeCodeCamp Python", "url": resource_urls.get("freeCodeCamp Python", "#")}
                ]
            },
            {
                "id": "ds_2", 
                "title": "Veri Manipülasyonu",
                "description": "Pandas ve NumPy ile veri işleme",
                "difficulty": "beginner",
                "estimated_hours": 25,
                "prerequisites": ["Python Temelleri"],
                "resources": [
                    {"name": "Pandas Documentation", "url": resource_urls.get("Pandas Documentation", "#")},
                    {"name": "DataCamp Python", "url": resource_urls.get("DataCamp Python", "#")},
                    {"name": "NumPy Documentation", "url": resource_urls.get("NumPy Documentation", "#")}
                ]
            },
            {
                "id": "ds_3",
                "title": "Veri Görselleştirme",
                "description": "Matplotlib ve Seaborn ile veri görselleştirme",
                "difficulty": "intermediate",
                "estimated_hours": 15,
                "prerequisites": ["Veri Manipülasyonu"],
                "resources": [
                    {"name": "Matplotlib Tutorial", "url": resource_urls.get("Matplotlib Tutorial", "#")},
                    {"name": "Seaborn Tutorial", "url": resource_urls.get("Seaborn Tutorial", "#")},
                    {"name": "scikit-learn Tutorial", "url": resource_urls.get("scikit-learn Tutorial", "#")}
                ]
            }
        ]
        
        return {
            "title": "Veri Bilimi Yol Haritası",
            "description": "Sıfırdan veri bilimci olma yolculuğunuz",
            "modules": random.sample(data_modules, min(3, len(data_modules)))
        }
    
    # Machine Learning roadmap
    elif any(word in interests_text for word in ["makine", "ai", "ml", "tensorflow", "scikit"]):
        ml_modules = [
            {
                "id": "ml_1",
                "title": "Matematik Temelleri",
                "description": "Lineer cebir, kalkülüs ve istatistik",
                "difficulty": "beginner",
                "estimated_hours": 40,
                "prerequisites": [],
                "resources": [
                    {"name": "Andrew Ng ML Course", "url": resource_urls.get("Andrew Ng ML Course", "#")},
                    {"name": "TensorFlow Tutorial", "url": resource_urls.get("TensorFlow Tutorial", "#")},
                    {"name": "PyTorch Tutorial", "url": resource_urls.get("PyTorch Tutorial", "#")}
                ]
            },
            {
                "id": "ml_2",
                "title": "Python ve Veri Bilimi",
                "description": "Python, Pandas, NumPy ile veri işleme",
                "difficulty": "beginner",
                "estimated_hours": 30,
                "prerequisites": ["Matematik Temelleri"],
                "resources": [
                    {"name": "DataCamp Python", "url": resource_urls.get("DataCamp Python", "#")},
                    {"name": "freeCodeCamp Python", "url": resource_urls.get("freeCodeCamp Python", "#")},
                    {"name": "Pandas Documentation", "url": resource_urls.get("Pandas Documentation", "#")}
                ]
            },
            {
                "id": "ml_3",
                "title": "Makine Öğrenmesi Algoritmaları",
                "description": "Scikit-learn ile ML algoritmaları",
                "difficulty": "intermediate",
                "estimated_hours": 35,
                "prerequisites": ["Python ve Veri Bilimi"],
                "resources": [
                    {"name": "Andrew Ng ML Course", "url": resource_urls.get("Andrew Ng ML Course", "#")},
                    {"name": "scikit-learn Tutorial", "url": resource_urls.get("scikit-learn Tutorial", "#")},
                    {"name": "Kaggle Courses", "url": resource_urls.get("Kaggle Courses", "#")}
                ]
            }
        ]
        
        return {
            "title": "Makine Öğrenmesi Yol Haritası",
            "description": "Makine öğrenmesi ve yapay zeka yolculuğu",
            "modules": random.sample(ml_modules, min(3, len(ml_modules)))
        }
    
    # Default roadmap
    else:
        default_modules = [
            {
                "id": "gen_1",
                "title": "Programlama Temelleri",
                "description": "Algoritma ve programlama mantığı",
                "difficulty": "beginner",
                "estimated_hours": 25,
                "prerequisites": [],
                "resources": ["freeCodeCamp", "Khan Academy", "Codecademy"]
            },
            {
                "id": "gen_2",
                "title": "Python ile Başlangıç",
                "description": "Python programlama dilini öğrenin",
                "difficulty": "beginner",
                "estimated_hours": 20,
                "prerequisites": ["Programlama Temelleri"],
                "resources": ["Python.org Tutorial", "freeCodeCamp Python", "Codecademy Python"]
            }
        ]
        
        return {
            "title": "Genel Programlama Yol Haritası",
            "description": "Programlama temellerini öğrenme yolculuğu",
            "modules": random.sample(default_modules, min(2, len(default_modules)))
        }

def enhance_module_with_content(module: Module, topic: str, skill_level: str) -> Module:
    """Modülü AI destekli eğitim içerik önerileri ile zenginleştir"""
    
    try:
        # Modül başlığından konu çıkar
        module_topic = module.title.lower()
        
        # AI ile eğitim içerik önerileri al
        content_recommendations = educational_content_service.get_content_recommendations(
            module_topic, skill_level, 3
        )
        
        # Mevcut kaynakları koru ve yeni önerileri ekle
        enhanced_resources = module.resources.copy()
        for rec in content_recommendations:
            enhanced_resources.append(f"{rec['title']} ({rec['platform']}) - {rec['url']}")
        
        # Modülü güncelle
        module.resources = enhanced_resources
        return module
    except Exception as e:
        print(f"Error enhancing module with content: {e}")
        # Hata durumunda orijinal modülü döndür
        return module

@router.post("/generate", response_model=Roadmap)
async def generate_roadmap(
    request: RoadmapRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Kullanıcı bilgilerine göre kişiselleştirilmiş yol haritası oluştur"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user_id = payload.get("sub")
    
    try:
        # AI ile dinamik roadmap oluştur
        roadmap_data = generate_ai_roadmap(request.interests, request.skill_level, request.learning_goals)
    except Exception as e:
        print(f"Roadmap generation error: {e}")
        # Fallback roadmap kullan
        roadmap_data = get_fallback_roadmap(request.interests, request.skill_level)
    
    # Roadmap data kontrolü
    if not roadmap_data or "title" not in roadmap_data or "modules" not in roadmap_data:
        print("Roadmap data eksik, fallback kullanılıyor")
        roadmap_data = get_fallback_roadmap(request.interests, request.skill_level)
    
    # Modülleri oluştur ve eğitim içerikleri ile zenginleştir
    modules = []
    for i, module_data in enumerate(roadmap_data["modules"]):
        # Resources'ları string formatına çevir
        resources = module_data.get("resources", [])
        if resources and isinstance(resources[0], dict):
            # Dictionary listesi ise string listesine çevir
            resources = [f"{r.get('name', 'Resource')}: {r.get('url', '#')}" for r in resources]
        
        module = Module(
            id=module_data["id"],
            title=module_data["title"],
            description=module_data["description"],
            difficulty=module_data["difficulty"],
            estimated_hours=module_data["estimated_hours"],
            prerequisites=module_data.get("prerequisites", []),
            resources=resources,
            completed=False,
            progress_percentage=0
        )
        
        # Modülü eğitim içerikleri ile zenginleştir
        enhanced_module = enhance_module_with_content(module, roadmap_data["title"], request.skill_level)
        modules.append(enhanced_module)
    
    # Öğrenme hedefleri oluştur
    learning_goals = []
    for goal in request.learning_goals:
        learning_goal = LearningGoal(
            title=goal,
            description=f"{goal} alanında uzmanlaşmak",
            target_date=None
        )
        learning_goals.append(learning_goal)
    
    # Beceri değerlendirmeleri oluştur
    skill_assessments = []
    skill_names = []
    
    # İlgi alanlarına göre beceri isimleri belirle
    for interest in request.interests:
        interest_lower = interest.lower()
        if "python" in interest_lower:
            skill_names.extend(["Python", "Algoritma", "Veri Yapıları"])
        elif "web" in interest_lower or "frontend" in interest_lower or "backend" in interest_lower:
            skill_names.extend(["HTML/CSS", "JavaScript", "Web Development"])
        elif "veri" in interest_lower or "data" in interest_lower:
            skill_names.extend(["Veri Analizi", "İstatistik", "Python"])
        elif "makine" in interest_lower or "ai" in interest_lower or "ml" in interest_lower:
            skill_names.extend(["Makine Öğrenmesi", "Python", "Matematik"])
        else:
            skill_names.append(interest)
    
    # Tekrarlanan becerileri kaldır
    skill_names = list(set(skill_names))
    
    for skill in skill_names[:4]:  # Maksimum 4 beceri
        assessment = SkillAssessment(
            skill_name=skill,
            current_level=request.skill_level,
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
        title=roadmap_data["title"],
        description=roadmap_data["description"],
        created_at=datetime.now(),
        modules=modules,
        learning_goals=learning_goals,
        skill_assessments=skill_assessments,
        total_estimated_hours=total_hours,
        completed_modules=0,
        overall_progress=0
    )
    
    # Chatbot cache'ine kullanıcı bilgilerini kaydet
    from routers.chatbot import roadmap_cache
    roadmap_cache[user_id] = {
        "skill_level": request.skill_level,
        "interests": request.interests,
        "learning_goals": request.learning_goals,
        "available_hours_per_week": request.available_hours_per_week,
        "target_timeline_months": request.target_timeline_months,
        "roadmap_id": roadmap.id,
        "roadmap_title": roadmap.title
    }
    
    return roadmap

@router.post("/generate-from-chat")
async def generate_roadmap_from_chat(
    user_message: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Chatbot mesajından yol haritası oluştur"""
    
    try:
        # Token doğrulama
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=401, detail="Geçersiz token")
        
        print(f"Processing roadmap request for message: {user_message}")
        
        # Kullanıcı mesajını analiz et
        analysis = ai_service.analyze_learning_request(user_message)
        print(f"Analysis result: {analysis}")
        
        if not analysis.get("has_learning_request", False):
            raise HTTPException(status_code=400, detail="Öğrenme isteği tespit edilemedi")
        
        # Roadmap request oluştur
        roadmap_request = RoadmapRequest(
            skill_level=analysis.get("skill_level", "beginner"),
            interests=analysis.get("learning_areas", []) + analysis.get("subtopics", []),
            learning_goals=[f"{area} öğrenmek" for area in analysis.get("learning_areas", [])],
            available_hours_per_week=10,  # varsayılan
            target_timeline_months=analysis.get("timeline_months", 6)
        )
        
        print(f"Roadmap request: {roadmap_request}")
        
        # Roadmap oluştur
        roadmap = await generate_roadmap(roadmap_request, credentials)
        
        return {
            "roadmap": roadmap,
            "analysis": analysis,
            "message": f"'{user_message}' isteğinize göre {len(roadmap.modules)} modüllük bir yol haritası oluşturdum!"
        }
    except HTTPException:
        # HTTPException'ları tekrar fırlat
        raise
    except Exception as e:
        print(f"Error generating roadmap from chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Yol haritası oluşturulurken bir hata oluştu")

@router.get("/{roadmap_id}")
async def get_roadmap_by_id(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Belirli bir roadmap'i ID ile getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    # For now, return a mock roadmap based on the ID
    # In a real implementation, this would fetch from a database
    mock_roadmap = {
        "roadmap_id": roadmap_id,
        "title": f"Roadmap #{roadmap_id}",
        "description": "Bu roadmap, seçilen becerileri geliştirmek için tasarlanmış kapsamlı bir öğrenme yolculuğudur.",
        "skill_level": "beginner",
        "estimated_duration_hours": 9,
        "created_at": "2024-01-01T00:00:00Z",
        "modules": [
            {
                "id": "1",
                "title": "Temel Kavramlar",
                "description": "Bu modülde temel kavramları öğreneceksiniz.",
                "duration_minutes": 120,
                "difficulty": "Başlangıç",
                "resources": ["Video ders", "PDF doküman", "Pratik alıştırmalar"],
                "quiz_questions": ["Soru 1", "Soru 2", "Soru 3"]
            },
            {
                "id": "2",
                "title": "İleri Seviye Teknikler",
                "description": "İleri seviye teknikleri ve uygulamaları keşfedin.",
                "duration_minutes": 180,
                "difficulty": "Orta",
                "resources": ["Video ders", "Kod örnekleri", "Proje çalışması"],
                "quiz_questions": ["Soru 1", "Soru 2", "Soru 3", "Soru 4"]
            },
            {
                "id": "3",
                "title": "Uygulama Projeleri",
                "description": "Öğrendiklerinizi gerçek projelerde uygulayın.",
                "duration_minutes": 240,
                "difficulty": "İleri",
                "resources": ["Proje rehberi", "Kod deposu", "Canlı demo"],
                "quiz_questions": ["Soru 1", "Soru 2"]
            }
        ]
    }
    
    return mock_roadmap

@router.get("/content-recommendations/{topic}")
async def get_content_recommendations(
    topic: str,
    skill_level: str = "beginner",
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Belirli bir konu için eğitim içerik önerileri getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    recommendations = educational_content_service.get_content_recommendations(
        topic, skill_level, 10
    )
    
    return {
        "topic": topic,
        "skill_level": skill_level,
        "recommendations": recommendations,
        "total_count": len(recommendations)
    }

@router.get("/progress/{roadmap_id}")
async def get_roadmap_progress(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Yol haritası ilerlemesini getir"""
    
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    # Dummy progress data
    progress_data = {
        "roadmap_id": roadmap_id,
        "overall_progress": random.randint(10, 80),
        "completed_modules": random.randint(1, 3),
        "total_modules": 4,
        "estimated_completion_date": "2024-12-31",
        "weekly_progress": [
            {"week": 1, "progress": 15},
            {"week": 2, "progress": 25},
            {"week": 3, "progress": 40},
            {"week": 4, "progress": 55}
        ]
    }
    
    return progress_data 