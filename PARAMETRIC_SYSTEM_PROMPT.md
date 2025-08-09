# Roadmap-Based Parametric System Prompt - MyWisePath

## Genel Bakış

MyWisePath platformunda Bilge Rehber ✨'in sistem prompt'u artık roadmap oluşturma sürecindeki kullanıcı bilgilerine göre parametrik hale getirilmiştir. Bu özellik sayesinde Bilge Rehber ✨, kullanıcının yol haritası oluştururken belirttiği bilgi düzeyi, ilgi alanları, öğrenme hedefleri ve zaman planına göre kişiselleştirilmiş cevaplar verebilmektedir.

## Özellikler

### 1. Roadmap Tabanlı Dinamik Sistem Prompt'u
- Yol haritası oluşturma sırasındaki kullanıcı bilgilerine göre otomatik olarak oluşturulur
- Seviye bazlı talimatlar içerir
- İlgi alanlarına özel yönergeler ekler
- Öğrenme hedeflerine uygun rehberlik sağlar
- Zaman planına göre özelleştirilmiş öneriler sunar

### 2. Seviye Bazlı Kişiselleştirme
- **Başlangıç (Beginner)**: Temel kavramlar, basit açıklamalar, motivasyonel destek
- **Orta Seviye (Intermediate)**: Detaylı kavramlar, pratik örnekler, ileri kaynaklar
- **İleri Seviye (Advanced)**: Karmaşık konular, performans optimizasyonu, güncel trendler

### 3. İlgi Alanı Bazlı Özelleştirme
- **AI & Machine Learning**: TensorFlow, PyTorch, güncel AI trendleri
- **Web Development**: Modern web teknolojileri, frontend/backend
- **Python Programming**: Python ekosistemi, kütüphaneler
- **Data Science**: Veri analizi, görselleştirme, Pandas/NumPy

### 4. Hedef Odaklı Rehberlik
- **Kariyer Odaklı**: Endüstri trendleri, kariyer önerileri
- **Proje Odaklı**: Portfolio geliştirme, proje tabanlı öğrenme
- **Sertifika Odaklı**: Sınav hazırlık, sertifika programları

### 5. Zaman Planı Bazlı Özelleştirme
- **Düşük Zaman (≤5 saat/hafta)**: Esnek öğrenme yöntemleri, kısa ve etkili teknikler
- **Orta Zaman (6-15 saat/hafta)**: Dengeli programlar, pratik-teorik denge
- **Yüksek Zaman (≥16 saat/hafta)**: Yoğun programlar, derinlemesine öğrenme

## Teknik Implementasyon

### Backend (Python/FastAPI)

#### 1. AI Service Güncellemeleri
```python
# backend/services/ai_service.py

def get_ai_response(self, user_message: str, user_context: Optional[dict] = None, user_profile: Optional[dict] = None, roadmap_info: Optional[dict] = None) -> str:
    """
    Roadmap bilgilerine göre kişiselleştirilmiş AI cevabı
    """
    if roadmap_info:
        system_prompt = self._generate_roadmap_based_system_prompt(roadmap_info)
    else:
        system_prompt = self._generate_dynamic_system_prompt(user_profile)
    # ... AI response generation
```

#### 2. Roadmap Tabanlı Prompt Oluşturma
```python
def _generate_roadmap_based_system_prompt(self, roadmap_info: dict) -> str:
    """
    Roadmap oluşturma sırasındaki kullanıcı bilgilerine göre dinamik sistem prompt'u oluştur
    """
            base_prompt = "Sen MyWisePath öğrenme platformunun Bilge Rehber ✨'sin..."
    
    skill_level = roadmap_info.get('skill_level', 'beginner')
    interests = roadmap_info.get('interests', [])
    learning_goals = roadmap_info.get('learning_goals', [])
    available_hours = roadmap_info.get('available_hours_per_week', 10)
    timeline_months = roadmap_info.get('target_timeline_months', 6)
    
    # Seviye bazlı talimatlar
    level_instructions = self._get_level_specific_instructions(skill_level)
    
    # İlgi alanı bazlı talimatlar
    interest_instructions = self._get_interest_specific_instructions(interests)
    
    # Hedef bazlı talimatlar
    goal_instructions = self._get_goal_specific_instructions(learning_goals)
    
    # Zaman planı bazlı talimatlar
    time_instructions = self._get_time_based_instructions(available_hours, timeline_months)
    
    return base_prompt + level_instructions + interest_instructions + goal_instructions + time_instructions
```

#### 3. Roadmap Router Güncellemeleri
```python
# backend/routers/roadmap.py

@router.post("/generate", response_model=Roadmap)
async def generate_roadmap(request: RoadmapRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # ... roadmap generation logic
    
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
```

#### 4. Chatbot Router Güncellemeleri
```python
# backend/routers/chatbot.py

@router.post("/query", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Kullanıcının roadmap bilgilerini al
    roadmap_info = await get_user_roadmap_info(user_id)
    
    # Eğer roadmap bilgisi yoksa, kullanıcıya roadmap oluşturmasını öner
    if not roadmap_info:
        return ChatResponse(
            message="Merhaba! Size daha iyi yardımcı olabilmem için önce bir yol haritası oluşturmanızı öneriyorum...",
            timestamp=datetime.now(),
            has_roadmap_suggestion=True
        )
    
    # AI ile kişiselleştirilmiş cevap al - roadmap bilgilerini kullan
    enhanced_response = await ai_service.get_ai_response_with_serp_search(
        request.message, 
        roadmap_info=roadmap_info
    )
```

### Frontend (React/TypeScript)

#### 1. Roadmap Oluşturma Süreci
```typescript
// frontend/src/pages/Roadmap.tsx

const Roadmap: React.FC = () => {
  const [formData, setFormData] = useState<RoadmapForm>({
    skill_level: 'beginner',
    interests: [],
    learning_goals: [],
    available_hours_per_week: 10,
    target_timeline_months: 6,
  });
  
  const generateRoadmap = async () => {
    const roadmapRequest: RoadmapRequest = {
      skill_level: formData.skill_level,
      interests: formData.interests,
      learning_goals: formData.learning_goals,
      available_hours_per_week: formData.available_hours_per_week,
      target_timeline_months: formData.target_timeline_months,
    };
    
    const response = await roadmapService.generateRoadmap(roadmapRequest);
    // Roadmap bilgileri otomatik olarak backend'de cache'e kaydedilir
  };
};
```

## Kullanım Senaryoları

### Senaryo 1: Part-Time Python Öğrencisi
**Roadmap Bilgileri:**
- Seviye: Beginner
- İlgi Alanları: ["Python", "Web Development"]
- Hedefler: ["Python Programming", "Web Development"]
- Haftalık Süre: 5 saat
- Hedef Süre: 6 ay

**AI Asistan Davranışı:**
- Temel Python kavramlarını basit şekilde açıklar
- Esnek öğrenme yöntemleri önerir
- Kısa ve etkili öğrenme teknikleri paylaşır
- Motivasyonel ve destekleyici olur

### Senaryo 2: Full-Time AI Geliştiricisi
**Roadmap Bilgileri:**
- Seviye: Intermediate
- İlgi Alanları: ["AI", "Machine Learning", "Data Science"]
- Hedefler: ["Deep Learning", "TensorFlow"]
- Haftalık Süre: 25 saat
- Hedef Süre: 3 ay

**AI Asistan Davranışı:**
- Orta seviye ML kavramlarını detaylandırır
- Yoğun ve hızlı ilerleme odaklı programlar önerir
- TensorFlow, PyTorch gibi framework'ler hakkında bilgi verir
- Odaklanmış ve hedefe yönelik yaklaşımlar sunar

### Senaryo 3: Intensive Web Geliştiricisi
**Roadmap Bilgileri:**
- Seviye: Advanced
- İlgi Alanları: ["React", "Node.js", "Full Stack"]
- Hedefler: ["Microservices", "Cloud Architecture"]
- Haftalık Süre: 40 saat
- Hedef Süre: 12 ay

**AI Asistan Davranışı:**
- İleri seviye web teknolojilerine odaklanır
- Uzun vadeli ve kapsamlı öğrenme programları önerir
- Karmaşık mimari konularını açıklar
- Derinlemesine uzmanlaşma fırsatları sunar

## API Endpoints

### 1. Roadmap Oluşturma
```http
POST /api/v1/roadmap/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "skill_level": "intermediate",
  "interests": ["AI", "Machine Learning"],
  "learning_goals": ["Deep Learning", "TensorFlow"],
  "available_hours_per_week": 25,
  "target_timeline_months": 3
}
```

### 2. Chatbot Sorgusu (Güncellenmiş)
```http
POST /api/v1/chatbot/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "Python öğrenmek istiyorum"
}
```

## Test Etme

### Test Script'i Çalıştırma
```bash
cd MyWisePath
python test_parametric_prompt.py
```

### Manuel Test
1. Dashboard'a giriş yap
2. "Yeni Yol Haritası Oluştur" butonuna tıkla
3. Bilgi seviyesi, ilgi alanları, hedefler ve zaman planını ayarla
4. Yol haritasını oluştur
5. Chatbot'u aç ve soru sor
6. Roadmap bilgilerine göre kişiselleştirilmiş cevapları gözlemle

## Gelecek Geliştirmeler

### 1. Gelişmiş Zaman Analizi
- Öğrenme hızına göre dinamik ayarlama
- Gerçek zamanlı ilerleme takibi
- Adaptif öğrenme stratejileri

### 2. Çoklu Roadmap Desteği
- Birden fazla yol haritası yönetimi
- Roadmap'ler arası geçiş
- Karmaşık öğrenme yolları

### 3. Gerçek Zamanlı Öğrenme
- Kullanıcı etkileşimlerini analiz etme
- Sürekli roadmap güncelleme
- Performans bazlı öneriler

### 4. Sosyal Öğrenme
- Benzer roadmap'lere sahip kullanıcıları eşleştirme
- Grup öğrenme fırsatları
- Mentorluk sistemi

## Sonuç

Roadmap-based parametric system prompt özelliği, MyWisePath platformunda kullanıcı deneyimini önemli ölçüde iyileştirmektedir. Bilge Rehber ✨ artık her kullanıcının benzersiz öğrenme yolculuğuna ve zaman planına göre kişiselleştirilmiş rehberlik sağlayabilmektedir.

Bu özellik sayesinde:
- ✅ Kullanıcılar daha alakalı ve faydalı cevaplar alır
- ✅ Öğrenme deneyimi kişiselleştirilir
- ✅ AI asistanı daha etkili rehberlik sağlar
- ✅ Platform kullanıcı memnuniyetini artırır
- ✅ Zaman planına uygun öneriler sunulur 