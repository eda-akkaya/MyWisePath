from typing import List, Optional, Dict
from datetime import datetime, timedelta
import json
import os
from models.progress import (
    ModuleProgress, 
    RoadmapProgress, 
    ProgressStatus, 
    ProgressUpdate,
    QuizResult,
    QuizSubmission
)

class ProgressService:
    def __init__(self):
        self.progress_file = "user_progress.json"
        self.progress_data = self._load_progress_data()
    
    def _load_progress_data(self) -> Dict:
        """Kullanıcı ilerleme verilerini yükle"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_progress_data(self):
        """Kullanıcı ilerleme verilerini kaydet"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress_data, f, indent=2, default=str)
    
    def initialize_roadmap_progress(self, user_id: str, roadmap_id: str, total_modules: int) -> RoadmapProgress:
        """Yeni roadmap için ilerleme kaydı oluştur"""
        roadmap_key = f"{user_id}_{roadmap_id}"
        
        roadmap_progress = RoadmapProgress(
            roadmap_id=roadmap_id,
            user_id=user_id,
            total_modules=total_modules,
            started_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.progress_data[roadmap_key] = roadmap_progress.dict()
        self._save_progress_data()
        
        return roadmap_progress
    
    def get_roadmap_progress(self, user_id: str, roadmap_id: str) -> Optional[RoadmapProgress]:
        """Roadmap ilerlemesini getir"""
        roadmap_key = f"{user_id}_{roadmap_id}"
        
        if roadmap_key in self.progress_data:
            data = self.progress_data[roadmap_key]
            return RoadmapProgress(**data)
        
        return None
    
    def update_module_progress(self, user_id: str, roadmap_id: str, update: ProgressUpdate) -> ModuleProgress:
        """Modül ilerlemesini güncelle"""
        roadmap_key = f"{user_id}_{roadmap_id}"
        
        if roadmap_key not in self.progress_data:
            # Roadmap ilerlemesi yoksa oluştur
            self.initialize_roadmap_progress(user_id, roadmap_id, 0)
        
        roadmap_data = self.progress_data[roadmap_key]
        
        # Modül ilerlemesini bul veya oluştur
        module_progress = None
        for mp in roadmap_data.get("module_progress", []):
            if mp["module_id"] == update.module_id:
                module_progress = mp
                break
        
        if not module_progress:
            module_progress = {
                "module_id": update.module_id,
                "roadmap_id": roadmap_id,
                "user_id": user_id,
                "status": update.status.value,
                "progress_percentage": update.progress_percentage,
                "time_spent_minutes": update.time_spent_minutes,
                "started_at": datetime.now().isoformat() if update.status == ProgressStatus.IN_PROGRESS else None,
                "completed_at": datetime.now().isoformat() if update.status == ProgressStatus.COMPLETED else None,
                "last_activity": datetime.now().isoformat(),
                "notes": update.notes,
                "quiz_results": []
            }
            roadmap_data["module_progress"].append(module_progress)
        else:
            # Mevcut modül ilerlemesini güncelle
            module_progress["status"] = update.status.value
            module_progress["progress_percentage"] = update.progress_percentage
            module_progress["time_spent_minutes"] = update.time_spent_minutes
            module_progress["last_activity"] = datetime.now().isoformat()
            
            if update.status == ProgressStatus.IN_PROGRESS and not module_progress["started_at"]:
                module_progress["started_at"] = datetime.now().isoformat()
            
            if update.status == ProgressStatus.COMPLETED:
                module_progress["completed_at"] = datetime.now().isoformat()
            
            if update.notes:
                module_progress["notes"] = update.notes
        
        # Roadmap genel ilerlemesini güncelle
        self._update_roadmap_overall_progress(roadmap_data)
        
        self._save_progress_data()
        
        return ModuleProgress(**module_progress)
    
    def _update_roadmap_overall_progress(self, roadmap_data: Dict):
        """Roadmap genel ilerlemesini hesapla ve güncelle"""
        module_progresses = roadmap_data.get("module_progress", [])
        
        if not module_progresses:
            return
        
        total_modules = len(module_progresses)
        completed_modules = sum(1 for mp in module_progresses if mp["status"] == ProgressStatus.COMPLETED.value)
        total_progress = sum(mp["progress_percentage"] for mp in module_progresses)
        total_time = sum(mp["time_spent_minutes"] for mp in module_progresses)
        
        overall_progress = total_progress // total_modules if total_modules > 0 else 0
        
        roadmap_data["overall_progress"] = overall_progress
        roadmap_data["completed_modules"] = completed_modules
        roadmap_data["total_modules"] = total_modules
        roadmap_data["total_time_spent_minutes"] = total_time
        roadmap_data["last_activity"] = datetime.now().isoformat()
        
        # Tahmini tamamlanma tarihini hesapla
        if overall_progress > 0:
            remaining_progress = 100 - overall_progress
            if total_time > 0:
                progress_per_minute = overall_progress / total_time
                remaining_minutes = remaining_progress / progress_per_minute if progress_per_minute > 0 else 0
                estimated_completion = datetime.now() + timedelta(minutes=remaining_minutes)
                roadmap_data["estimated_completion_date"] = estimated_completion.isoformat()
    
    def submit_quiz_result(self, user_id: str, roadmap_id: str, submission: QuizSubmission) -> QuizResult:
        """Quiz sonucunu kaydet"""
        # Basit quiz değerlendirme (gerçek uygulamada daha karmaşık olabilir)
        score = self._evaluate_quiz(submission.answers)
        
        quiz_result = QuizResult(
            quiz_id=submission.quiz_id,
            module_id=submission.module_id,
            score=score,
            total_questions=len(submission.answers),
            correct_answers=score,  # Basit hesaplama
            completed_at=datetime.now(),
            time_taken_minutes=submission.time_taken_minutes
        )
        
        # Modül ilerlemesine quiz sonucunu ekle
        roadmap_key = f"{user_id}_{roadmap_id}"
        if roadmap_key in self.progress_data:
            roadmap_data = self.progress_data[roadmap_key]
            
            for mp in roadmap_data.get("module_progress", []):
                if mp["module_id"] == submission.module_id:
                    mp["quiz_results"].append(quiz_result.dict())
                    
                    # Quiz sonucuna göre ilerlemeyi güncelle
                    if score >= 80:  # %80 ve üzeri başarılı
                        mp["progress_percentage"] = min(100, mp["progress_percentage"] + 20)
                        if mp["progress_percentage"] >= 100:
                            mp["status"] = ProgressStatus.COMPLETED.value
                            mp["completed_at"] = datetime.now().isoformat()
                    
                    break
            
            self._update_roadmap_overall_progress(roadmap_data)
            self._save_progress_data()
        
        return quiz_result
    
    def _evaluate_quiz(self, answers: Dict[str, str]) -> int:
        """Quiz cevaplarını değerlendir (basit implementasyon)"""
        # Gerçek uygulamada burada doğru cevaplarla karşılaştırma yapılır
        # Şimdilik rastgele bir skor döndürüyoruz
        import random
        return random.randint(60, 100)
    
    def get_user_progress_summary(self, user_id: str) -> Dict:
        """Kullanıcının genel ilerleme özetini getir"""
        user_roadmaps = []
        total_time_spent = 0
        total_completed_modules = 0
        total_modules = 0
        
        for key, data in self.progress_data.items():
            if key.startswith(f"{user_id}_"):
                roadmap_progress = RoadmapProgress(**data)
                user_roadmaps.append(roadmap_progress)
                total_time_spent += roadmap_progress.total_time_spent_minutes
                total_completed_modules += roadmap_progress.completed_modules
                total_modules += roadmap_progress.total_modules
        
        return {
            "total_roadmaps": len(user_roadmaps),
            "total_time_spent_minutes": total_time_spent,
            "total_completed_modules": total_completed_modules,
            "total_modules": total_modules,
            "overall_completion_rate": (total_completed_modules / total_modules * 100) if total_modules > 0 else 0,
            "roadmaps": [rp.dict() for rp in user_roadmaps]
        }
    
    def get_weekly_progress(self, user_id: str, roadmap_id: str) -> List[Dict]:
        """Haftalık ilerleme verilerini getir"""
        # Son 4 haftanın verilerini simüle et
        weekly_data = []
        for week in range(4):
            week_data = {
                "week": week + 1,
                "progress": 0,
                "time_spent_minutes": 0,
                "modules_completed": 0
            }
            
            # Gerçek uygulamada burada veritabanından haftalık veriler çekilir
            # Şimdilik simüle ediyoruz
            import random
            week_data["progress"] = random.randint(10, 30) * (week + 1)
            week_data["time_spent_minutes"] = random.randint(60, 300)
            week_data["modules_completed"] = random.randint(0, 2)
            
            weekly_data.append(week_data)
        
        return weekly_data

# Global servis instance
progress_service = ProgressService()
