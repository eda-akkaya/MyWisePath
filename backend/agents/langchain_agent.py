"""
LangChain-based Agent for MyWisePath
Modern agent implementation using LangChain framework
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config import GEMINI_API_KEY
from services.ai_service import ai_service
from services.educational_content_service import educational_content_service
from services.serp_ai_service import serp_ai_service

class RoadmapRequest(BaseModel):
    interests: List[str] = Field(description="Kullanıcının ilgi alanları")
    skill_level: str = Field(description="Kullanıcının seviyesi (beginner/intermediate/advanced)")
    learning_goals: List[str] = Field(description="Öğrenme hedefleri")
    available_hours: int = Field(description="Haftalık çalışma saati")
    timeline_months: int = Field(description="Hedef süre (ay)")

class LangChainRoadmapAgent:
    """LangChain tabanlı roadmap oluşturma agent'ı"""
    
    def __init__(self):
        self.name = "LangChainRoadmapAgent"
        self.description = "LangChain-powered learning roadmap generation agent"
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.is_active = True
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        
        # LangChain bileşenleri
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",  # Doğru model adı
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )
        
        # Tools tanımlama
        self.tools = self._create_tools()
        
        # Agent prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Agent oluşturma
        self.agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
        
        # Roadmap storage
        self.roadmaps = {}
        
    def _get_system_prompt(self) -> str:
        """Agent için sistem prompt'u"""
        return """
        Sen MyWisePath platformunun AI destekli öğrenme yol haritası oluşturma uzmanısın.
        
        Görevlerin:
        1. Kullanıcının ilgi alanlarına göre kişiselleştirilmiş öğrenme yol haritaları oluştur
        2. Seviyelerine uygun modüller ve kaynaklar öner
        3. Pratik projeler ve öğrenme hedefleri belirle
        4. Zaman yönetimi ve ilerleme takibi için stratejiler sun
        
        Her yol haritası şu bilgileri içermeli:
        - Başlık ve açıklama
        - Modüller (başlık, açıklama, zorluk, süre, ön koşullar)
        - Öğrenme kaynakları
        - Pratik projeler
        - Kilometre taşları
        - Başarı kriterleri
        
        Türkçe yanıt ver ve JSON formatında çıktı üret.
        """
    
    def _create_tools(self) -> List:
        """Agent için araçları oluştur"""
        
        @tool
        def search_educational_content(query: str) -> str:
            """Eğitim içeriği ara"""
            try:
                results = educational_content_service.search_content(query)
                return json.dumps(results, ensure_ascii=False, indent=2)
            except Exception as e:
                return f"Eğitim içeriği arama hatası: {str(e)}"
        
        @tool
        def search_online_resources(topic: str) -> str:
            """Online kaynakları ara"""
            try:
                results = serp_ai_service.search_educational_content(topic)
                return json.dumps(results, ensure_ascii=False, indent=2)
            except Exception as e:
                return f"Online kaynak arama hatası: {str(e)}"
        
        @tool
        def analyze_skill_level(interests: List[str], goals: List[str]) -> str:
            """Kullanıcının seviyesini analiz et"""
            try:
                # Basit seviye analizi
                if any("temel" in goal.lower() or "başlangıç" in goal.lower() for goal in goals):
                    level = "beginner"
                elif any("ileri" in goal.lower() or "uzman" in goal.lower() for goal in goals):
                    level = "advanced"
                else:
                    level = "intermediate"
                
                return json.dumps({
                    "analyzed_level": level,
                    "confidence": 0.8,
                    "reasoning": f"İlgi alanları: {interests}, Hedefler: {goals}"
                }, ensure_ascii=False)
            except Exception as e:
                return f"Seviye analizi hatası: {str(e)}"
        
        @tool
        def generate_learning_modules(interests: List[str], level: str, hours: int) -> str:
            """Öğrenme modüllerini oluştur"""
            try:
                modules = []
                total_modules = max(3, min(8, hours // 10))  # Saate göre modül sayısı
                
                for i in range(total_modules):
                    module = {
                        "id": f"module_{i+1}",
                        "title": f"{interests[0] if interests else 'Öğrenme'} Modülü {i+1}",
                        "description": f"{level} seviyesi için {interests[0] if interests else 'genel'} öğrenme modülü",
                        "difficulty": level,
                        "estimated_hours": max(5, hours // total_modules),
                        "prerequisites": [],
                        "resources": ["Online kurslar", "Dokümantasyon", "Pratik alıştırmalar"],
                        "learning_objectives": [f"Modül {i+1} hedefleri"],
                        "practical_projects": [f"Modül {i+1} projesi"]
                    }
                    modules.append(module)
                
                return json.dumps(modules, ensure_ascii=False, indent=2)
            except Exception as e:
                return f"Modül oluşturma hatası: {str(e)}"
        
        return [search_educational_content, search_online_resources, analyze_skill_level, generate_learning_modules]
    
    async def create_roadmap(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """LangChain agent ile yol haritası oluştur"""
        
        try:
            # Kullanıcı bilgilerini hazırla
            interests = user_info.get('interests', [])
            skill_level = user_info.get('skill_level', 'beginner')
            learning_goals = user_info.get('learning_goals', [])
            available_hours = user_info.get('available_hours_per_week', 10)
            timeline_months = user_info.get('target_timeline_months', 6)
            
            # Agent'a görev ver
            task = f"""
            Aşağıdaki kullanıcı bilgilerine göre detaylı bir öğrenme yol haritası oluştur:
            
            İlgi Alanları: {', '.join(interests)}
            Seviye: {skill_level}
            Öğrenme Hedefleri: {', '.join(learning_goals)}
            Haftalık Çalışma Saati: {available_hours} saat
            Hedef Süre: {timeline_months} ay
            
            Lütfen şu JSON formatında bir yol haritası oluştur:
            {{
                "title": "Yol haritası başlığı",
                "description": "Detaylı açıklama",
                "estimated_duration_weeks": {timeline_months * 4},
                "weekly_hours": {available_hours},
                "modules": [
                    {{
                        "id": "unique_id",
                        "title": "Modül başlığı",
                        "description": "Modül açıklaması",
                        "difficulty": "beginner/intermediate/advanced",
                        "estimated_hours": sayı,
                        "prerequisites": ["ön koşul1", "ön koşul2"],
                        "resources": ["kaynak1", "kaynak2"],
                        "learning_objectives": ["hedef1", "hedef2"],
                        "practical_projects": ["proje1", "proje2"]
                    }}
                ],
                "learning_strategy": "Öğrenme stratejisi önerileri",
                "milestones": ["kilometre taşı1", "kilometre taşı2"],
                "success_metrics": ["başarı kriteri1", "başarı kriteri2"]
            }}
            
            Sadece JSON formatında cevap ver, başka açıklama ekleme.
            """
            
            try:
                # Agent'ı çalıştır
                result = await self.agent_executor.ainvoke({"input": task})
                
                # Sonucu parse et
                response_text = result.get("output", "")
                roadmap_data = self._parse_agent_response(response_text)
                
                if roadmap_data:
                    # Roadmap'i kaydet
                    roadmap_id = f"langchain_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    self.roadmaps[roadmap_id] = roadmap_data
                    
                    self.last_activity = datetime.now()
                    
                    return {
                        "success": True,
                        "roadmap_id": roadmap_id,
                        "roadmap": roadmap_data,
                        "message": "LangChain agent ile yol haritası oluşturuldu",
                        "agent": self.name
                    }
                else:
                    # Fallback to template-based roadmap
                    return self._create_fallback_roadmap(user_info)
                    
            except Exception as api_error:
                # API hatası durumunda fallback
                print(f"LangChain API error: {api_error}")
                return self._create_fallback_roadmap(user_info)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"LangChain agent hatası: {str(e)}"
            }
    
    def _create_fallback_roadmap(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """API hatası durumunda fallback roadmap oluştur"""
        try:
            interests = user_info.get('interests', [])
            skill_level = user_info.get('skill_level', 'beginner')
            learning_goals = user_info.get('learning_goals', [])
            available_hours = user_info.get('available_hours_per_week', 10)
            timeline_months = user_info.get('target_timeline_months', 6)
            
            # Template-based roadmap
            modules = []
            total_modules = max(3, min(6, available_hours // 8))
            
            for i in range(total_modules):
                module = {
                    "id": f"fallback_module_{i+1}",
                    "title": f"{interests[0] if interests else 'Öğrenme'} Modülü {i+1}",
                    "description": f"{skill_level} seviyesi için {interests[0] if interests else 'genel'} öğrenme modülü",
                    "difficulty": skill_level,
                    "estimated_hours": max(8, available_hours // total_modules),
                    "prerequisites": [],
                    "resources": ["Online kurslar", "Dokümantasyon", "Pratik alıştırmalar"],
                    "learning_objectives": [f"Modül {i+1} hedefleri"],
                    "practical_projects": [f"Modül {i+1} projesi"]
                }
                modules.append(module)
            
            roadmap_data = {
                "title": f"Kişiselleştirilmiş {', '.join(interests)} Öğrenme Yolu",
                "description": f"{skill_level} seviyesi için {', '.join(interests)} alanında öğrenme yol haritası",
                "estimated_duration_weeks": timeline_months * 4,
                "weekly_hours": available_hours,
                "modules": modules,
                "learning_strategy": "Aşamalı öğrenme ve pratik projeler",
                "milestones": [f"Modül {i+1} tamamlama" for i in range(total_modules)],
                "success_metrics": ["Tüm modülleri tamamlama", "Pratik projeler geliştirme"]
            }
            
            # Roadmap'i kaydet
            roadmap_id = f"fallback_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.roadmaps[roadmap_id] = roadmap_data
            
            self.last_activity = datetime.now()
            
            return {
                "success": True,
                "roadmap_id": roadmap_id,
                "roadmap": roadmap_data,
                "message": "Fallback template ile yol haritası oluşturuldu (API limiti nedeniyle)",
                "agent": self.name,
                "fallback": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Fallback roadmap oluşturma hatası: {str(e)}"
            }
    
    def _parse_agent_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Agent yanıtını parse et"""
        try:
            # JSON bul ve parse et
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                roadmap_data = json.loads(json_match.group())
                
                # Gerekli alanları kontrol et
                required_fields = ['title', 'description', 'modules']
                if all(field in roadmap_data for field in required_fields):
                    return roadmap_data
            
            return None
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"JSON parse hatası: {e}")
            return None
    
    async def analyze_roadmap(self, roadmap_id: str) -> Dict[str, Any]:
        """Mevcut yol haritasını analiz et"""
        if roadmap_id not in self.roadmaps:
            return {"error": "Yol haritası bulunamadı"}
        
        roadmap = self.roadmaps[roadmap_id]
        
        try:
            analysis_task = f"""
            Aşağıdaki yol haritasını analiz et ve öneriler sun:
            
            {json.dumps(roadmap, ensure_ascii=False, indent=2)}
            
            Analiz şu konuları içermeli:
            1. Toplam süre ve zorluk seviyesi uygunluğu
            2. Modüller arası bağımlılıklar
            3. Öğrenme kaynaklarının kalitesi
            4. Pratik projelerin uygunluğu
            5. İyileştirme önerileri
            
            JSON formatında analiz raporu oluştur.
            """
            
            result = await self.agent_executor.ainvoke({"input": analysis_task})
            analysis_text = result.get("output", "")
            
            return {
                "success": True,
                "roadmap_id": roadmap_id,
                "analysis": self._parse_agent_response(analysis_text) or {"raw_analysis": analysis_text}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Analiz hatası: {str(e)}"
            }
    
    def get_roadmap(self, roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Yol haritasını getir"""
        return self.roadmaps.get(roadmap_id)
    
    def get_all_roadmaps(self) -> Dict[str, Dict[str, Any]]:
        """Tüm yol haritalarını getir"""
        return self.roadmaps.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """Agent durumunu getir"""
        return {
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "roadmaps_count": len(self.roadmaps),
            "tools_count": len(self.tools),
            "framework": "LangChain"
        }

# Global LangChain agent instance
langchain_roadmap_agent = LangChainRoadmapAgent()
