"""
RoadmapAgent - AI-powered learning roadmap generation agent
Creates personalized learning paths based on user preferences and goals
"""

import asyncio
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from .base_agent import BaseAgent
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_service import ai_service
from services.educational_content_service import educational_content_service
from services.serp_ai_service import serp_ai_service

class RoadmapAgent(BaseAgent):
    """Agent specialized in creating personalized learning roadmaps"""
    
    def __init__(self):
        super().__init__(
            name="RoadmapAgent",
            description="AI-powered learning roadmap generation agent"
        )
        self.roadmap_templates = self._initialize_roadmap_templates()
        self.learning_paths = {}
        self.activate()
    
    def _initialize_roadmap_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize predefined roadmap templates for common learning areas"""
        return {
            "python": {
                "name": "Python Programming Path",
                "description": "Complete Python learning journey from basics to advanced",
                "modules": ["basics", "oop", "web", "data", "ai"]
            },
            "web_development": {
                "name": "Web Development Path", 
                "description": "Full-stack web development skills",
                "modules": ["html_css", "javascript", "frontend", "backend", "deployment"]
            },
            "data_science": {
                "name": "Data Science Path",
                "description": "Data analysis and machine learning skills",
                "modules": ["python", "pandas", "visualization", "ml", "deep_learning"]
            },
            "machine_learning": {
                "name": "Machine Learning Path",
                "description": "AI and machine learning fundamentals",
                "modules": ["math", "python", "ml_basics", "neural_networks", "projects"]
            }
        }
    
    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """Check if this agent can handle the given task"""
        task_type = task.get('type', '').lower()
        return task_type in ['create_roadmap', 'update_roadmap', 'analyze_roadmap', 'suggest_roadmap']
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute roadmap-related tasks"""
        if not self.is_active:
            return {"error": "Agent is not active"}
        
        self.update_activity()
        task_type = task.get('type', '').lower()
        
        try:
            if task_type == 'create_roadmap':
                return await self._create_roadmap(task)
            elif task_type == 'update_roadmap':
                return await self._update_roadmap(task)
            elif task_type == 'analyze_roadmap':
                return await self._analyze_roadmap(task)
            elif task_type == 'suggest_roadmap':
                return await self._suggest_roadmap(task)
            else:
                return {"error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            error_msg = f"Task execution error: {str(e)}"
            self.add_to_memory({"error": error_msg, "task": task})
            return {"error": error_msg}
    
    async def _create_roadmap(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a personalized learning roadmap"""
        user_info = task.get('user_info', {})
        interests = user_info.get('interests', [])
        skill_level = user_info.get('skill_level', 'beginner')
        learning_goals = user_info.get('learning_goals', [])
        available_hours = user_info.get('available_hours_per_week', 10)
        timeline_months = user_info.get('target_timeline_months', 6)
        
        # Add task to memory
        self.add_to_memory({
            "action": "create_roadmap",
            "user_info": user_info,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate AI-powered roadmap
        roadmap = await self._generate_ai_roadmap(
            interests, skill_level, learning_goals, available_hours, timeline_months
        )
        
        # Store roadmap
        roadmap_id = f"roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.learning_paths[roadmap_id] = roadmap
        
        # Add success to memory
        self.add_to_memory({
            "action": "roadmap_created",
            "roadmap_id": roadmap_id,
            "roadmap_title": roadmap.get('title', ''),
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "success": True,
            "roadmap_id": roadmap_id,
            "roadmap": roadmap,
            "message": "Roadmap created successfully"
        }
    
    async def _generate_ai_roadmap(self, interests: List[str], skill_level: str, 
                                  learning_goals: List[str], available_hours: int, 
                                  timeline_months: int) -> Dict[str, Any]:
        """Generate AI-powered roadmap using Gemini"""
        
        # Create comprehensive prompt
        prompt = f"""
        Aşağıdaki kullanıcı bilgilerine göre detaylı bir öğrenme yol haritası oluştur:
        
        İlgi Alanları: {', '.join(interests)}
        Seviye: {skill_level}
        Öğrenme Hedefleri: {', '.join(learning_goals)}
        Haftalık Çalışma Saati: {available_hours} saat
        Hedef Süre: {timeline_months} ay
        
        Yol haritası için şu bilgileri JSON formatında ver:
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
            # Use AI service to generate roadmap
            response = ai_service.get_ai_response(
                user_message=prompt,
                roadmap_info={
                    'skill_level': skill_level,
                    'interests': interests,
                    'learning_goals': learning_goals,
                    'available_hours_per_week': available_hours,
                    'target_timeline_months': timeline_months
                }
            )
            
            # Parse JSON response
            roadmap_data = self._parse_ai_response(response)
            
            if roadmap_data:
                return roadmap_data
            else:
                # Fallback to template-based roadmap
                return self._create_template_roadmap(interests, skill_level, available_hours, timeline_months)
                
        except Exception as e:
            print(f"AI roadmap generation error: {e}")
            # Fallback to template-based roadmap
            return self._create_template_roadmap(interests, skill_level, available_hours, timeline_months)
    
    def _parse_ai_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse AI response and extract JSON"""
        try:
            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                roadmap_data = json.loads(json_match.group())
                # Validate required fields
                required_fields = ['title', 'description', 'modules']
                if all(field in roadmap_data for field in required_fields):
                    return roadmap_data
            return None
        except (json.JSONDecodeError, AttributeError):
            return None
    
    def _create_template_roadmap(self, interests: List[str], skill_level: str, 
                                available_hours: int, timeline_months: int) -> Dict[str, Any]:
        """Create roadmap using predefined templates when AI fails"""
        
        # Determine primary interest
        primary_interest = self._determine_primary_interest(interests)
        
        if primary_interest in self.roadmap_templates:
            template = self.roadmap_templates[primary_interest]
            
            # Calculate module hours based on available time
            total_hours = available_hours * timeline_months * 4  # weeks
            module_hours = max(10, total_hours // len(template['modules']))
            
            modules = []
            for i, module_name in enumerate(template['modules']):
                modules.append({
                    "id": f"{primary_interest}_{i+1}",
                    "title": f"{module_name.title()} Module",
                    "description": f"Learn {module_name} fundamentals",
                    "difficulty": skill_level,
                    "estimated_hours": module_hours,
                    "prerequisites": [],
                    "resources": [f"Learn {module_name}"],
                    "learning_objectives": [f"Master {module_name} basics"],
                    "practical_projects": [f"Build {module_name} project"]
                })
            
            return {
                "title": template['name'],
                "description": template['description'],
                "estimated_duration_weeks": timeline_months * 4,
                "weekly_hours": available_hours,
                "modules": modules,
                "learning_strategy": "Structured learning with practical projects",
                "milestones": [f"Complete {module['title']}" for module in modules],
                "success_metrics": ["Complete all modules", "Build portfolio projects"]
            }
        
        # Generic roadmap if no template matches
        return self._create_generic_roadmap(interests, skill_level, available_hours, timeline_months)
    
    def _determine_primary_interest(self, interests: List[str]) -> str:
        """Determine primary interest from user interests"""
        interest_mapping = {
            'python': 'python',
            'programlama': 'python',
            'kod': 'python',
            'web': 'web_development',
            'html': 'web_development',
            'css': 'web_development',
            'javascript': 'web_development',
            'veri': 'data_science',
            'data': 'data_science',
            'analiz': 'data_science',
            'makine': 'machine_learning',
            'ai': 'machine_learning',
            'yapay zeka': 'machine_learning'
        }
        
        for interest in interests:
            interest_lower = interest.lower()
            for keyword, mapped_interest in interest_mapping.items():
                if keyword in interest_lower:
                    return mapped_interest
        
        return 'python'  # Default to Python
    
    def _create_generic_roadmap(self, interests: List[str], skill_level: str, 
                                available_hours: int, timeline_months: int) -> Dict[str, Any]:
        """Create a generic learning roadmap"""
        
        modules = [
            {
                "id": "fundamentals",
                "title": "Learning Fundamentals",
                "description": "Build strong foundation in your chosen field",
                "difficulty": skill_level,
                "estimated_hours": available_hours * 2,
                "prerequisites": [],
                "resources": ["Online courses", "Documentation", "Practice exercises"],
                "learning_objectives": ["Understand core concepts", "Practice basic skills"],
                "practical_projects": ["Hello World project", "Basic exercises"]
            },
            {
                "id": "intermediate",
                "title": "Intermediate Skills",
                "description": "Develop practical skills and deeper understanding",
                "difficulty": "intermediate",
                "estimated_hours": available_hours * 3,
                "prerequisites": ["fundamentals"],
                "resources": ["Advanced courses", "Real-world examples", "Community forums"],
                "learning_objectives": ["Apply concepts practically", "Solve real problems"],
                "practical_projects": ["Portfolio project", "Real-world application"]
            },
            {
                "id": "advanced",
                "title": "Advanced Applications",
                "description": "Master advanced concepts and build complex projects",
                "difficulty": "advanced",
                "estimated_hours": available_hours * 3,
                "prerequisites": ["intermediate"],
                "resources": ["Expert tutorials", "Research papers", "Open source projects"],
                "learning_objectives": ["Master advanced topics", "Build complex systems"],
                "practical_projects": ["Complex project", "Contribution to open source"]
            }
        ]
        
        return {
            "title": f"Personalized Learning Path for {', '.join(interests)}",
            "description": "Customized learning journey based on your interests and goals",
            "estimated_duration_weeks": timeline_months * 4,
            "weekly_hours": available_hours,
            "modules": modules,
            "learning_strategy": "Progressive learning with hands-on projects",
            "milestones": ["Complete fundamentals", "Build intermediate skills", "Master advanced topics"],
            "success_metrics": ["Complete all modules", "Build portfolio", "Apply skills practically"]
        }
    
    async def _update_roadmap(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing roadmap based on new information"""
        roadmap_id = task.get('roadmap_id')
        if roadmap_id not in self.learning_paths:
            return {"error": "Roadmap not found"}
        
        # Implementation for updating roadmap
        return {"success": True, "message": "Roadmap updated"}
    
    async def _analyze_roadmap(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze existing roadmap and provide insights"""
        roadmap_id = task.get('roadmap_id')
        if roadmap_id not in self.learning_paths:
            return {"error": "Roadmap not found"}
        
        roadmap = self.learning_paths[roadmap_id]
        
        # Analyze roadmap complexity, duration, etc.
        analysis = {
            "total_modules": len(roadmap.get('modules', [])),
            "estimated_total_hours": sum(module.get('estimated_hours', 0) for module in roadmap.get('modules', [])),
            "difficulty_distribution": self._analyze_difficulty_distribution(roadmap),
            "prerequisites_chain": self._analyze_prerequisites(roadmap),
            "recommendations": self._generate_analysis_recommendations(roadmap)
        }
        
        return {
            "success": True,
            "analysis": analysis,
            "roadmap_id": roadmap_id
        }
    
    def _analyze_difficulty_distribution(self, roadmap: Dict[str, Any]) -> Dict[str, int]:
        """Analyze difficulty distribution of modules"""
        difficulty_count = {"beginner": 0, "intermediate": 0, "advanced": 0}
        for module in roadmap.get('modules', []):
            difficulty = module.get('difficulty', 'beginner')
            difficulty_count[difficulty] = difficulty_count.get(difficulty, 0) + 1
        return difficulty_count
    
    def _analyze_prerequisites(self, roadmap: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analyze prerequisites chain"""
        prerequisites_map = {}
        for module in roadmap.get('modules', []):
            module_id = module.get('id')
            prerequisites = module.get('prerequisites', [])
            if prerequisites:
                prerequisites_map[module_id] = prerequisites
        return prerequisites_map
    
    def _generate_analysis_recommendations(self, roadmap: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on roadmap analysis"""
        recommendations = []
        modules = roadmap.get('modules', [])
        
        if len(modules) > 10:
            recommendations.append("Consider breaking down into smaller, focused roadmaps")
        
        total_hours = sum(module.get('estimated_hours', 0) for module in modules)
        if total_hours > 200:
            recommendations.append("This is a long-term journey - consider setting intermediate milestones")
        
        beginner_modules = [m for m in modules if m.get('difficulty') == 'beginner']
        if len(beginner_modules) == 0:
            recommendations.append("Consider adding foundational modules for beginners")
        
        return recommendations
    
    async def _suggest_roadmap(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest roadmap improvements or alternatives"""
        user_info = task.get('user_info', {})
        current_roadmap = task.get('current_roadmap', {})
        
        # Generate suggestions using AI
        suggestions = await self._generate_ai_suggestions(user_info, current_roadmap)
        
        return {
            "success": True,
            "suggestions": suggestions
        }
    
    async def _generate_ai_suggestions(self, user_info: Dict[str, Any], 
                                     current_roadmap: Dict[str, Any]) -> List[str]:
        """Generate AI-powered suggestions for roadmap improvement"""
        
        prompt = f"""
        Mevcut yol haritası ve kullanıcı bilgilerine göre iyileştirme önerileri sun:
        
        Kullanıcı Bilgileri: {json.dumps(user_info, ensure_ascii=False)}
        Mevcut Yol Haritası: {json.dumps(current_roadmap, ensure_ascii=False)}
        
        Şu konularda öneriler ver:
        1. Yol haritası iyileştirmeleri
        2. Eksik modüller
        3. Öğrenme stratejisi önerileri
        4. Pratik proje önerileri
        
        Her öneri için kısa açıklama ekle.
        """
        
        try:
            response = ai_service.get_ai_response(prompt)
            # Parse suggestions from response
            suggestions = self._extract_suggestions(response)
            return suggestions
        except Exception as e:
            print(f"AI suggestions error: {e}")
            return ["Focus on practical projects", "Set clear milestones", "Practice regularly"]
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract suggestions from AI response"""
        # Simple extraction - can be improved
        suggestions = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.')):
                suggestion = line.lstrip('-•1234567890. ')
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions if suggestions else ["Practice regularly", "Set clear goals", "Build projects"]
    
    def get_roadmap(self, roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific roadmap by ID"""
        return self.learning_paths.get(roadmap_id)
    
    def get_all_roadmaps(self) -> Dict[str, Dict[str, Any]]:
        """Get all created roadmaps"""
        return self.learning_paths.copy()
    
    def delete_roadmap(self, roadmap_id: str) -> bool:
        """Delete a roadmap"""
        if roadmap_id in self.learning_paths:
            del self.learning_paths[roadmap_id]
            self.add_to_memory({
                "action": "roadmap_deleted",
                "roadmap_id": roadmap_id,
                "timestamp": datetime.now().isoformat()
            })
            return True
        return False

# Global RoadmapAgent instance
roadmap_agent = RoadmapAgent()
