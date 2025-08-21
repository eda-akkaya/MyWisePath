# MyWisePath - Kişiselleştirilmiş Öğrenme Platformu Proje Özeti

## 🎯 Proje Genel Bakış

**MyWisePath**, kullanıcıların kişisel öğrenme yolculuklarını planlamalarına ve takip etmelerine yardımcı olan AI destekli bir öğrenme platformudur. Platform, modern web teknolojileri ve yapay zeka entegrasyonu ile kişiselleştirilmiş öğrenme deneyimi sunar.

### Ana Özellikler:
- 🤖 **AI Destekli Öğrenme Önerileri** (Gemini AI)
- 🗺️ **Kişiselleştirilmiş Roadmap'ler**
- 💬 **İnteraktif Chatbot**
- 📧 **E-posta Otomasyonu**
- 🔍 **RAG (Retrieval-Augmented Generation) Sistemi**
- 📊 **İlerleme Takibi**
- 🎓 **Öğrenme Ortamı Yönetimi**

---

## 🏗️ Sistem Mimarisi

### 1. Genel Mimari Diyagramı

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Dashboard │  │  Roadmap    │  │  Chatbot    │  │ Progress│ │
│  │             │  │  Creator    │  │             │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Learning  │  │ Educational │  │    RAG      │  │  Agent  │ │
│  │ Environment │  │   Content   │  │   Search    │  │Dashboard│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    Auth     │  │   Roadmap   │  │  Chatbot    │  │Automation│ │
│  │   Router    │  │   Router    │  │   Router    │  │  Router  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │  Learning   │  │   Agents    │  │  Progress   │  │   RAG   │ │
│  │ Environment │  │   Router    │  │   Router    │  │  Router  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        SERVICE LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    AI       │  │ Educational │  │    Email    │  │Automation│ │
│  │  Service    │  │   Content   │  │   Service   │  │  Service │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │  Learning   │  │   Progress  │  │    Serp     │  │   Live  │ │
│  │ Environment │  │   Service   │  │     AI      │  │  Content │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AGENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Agent     │  │  Roadmap    │  │  LangChain  │  │  Base   │ │
│  │  Manager    │  │   Agent     │  │   Agent     │  │  Agent  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        RAG SYSTEM                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Search    │  │Recommendation│  │    PDF      │  │ Vector  │ │
│  │  Service    │  │   Service    │  │ Generator   │  │  Store  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Veri Modeli İlişkileri

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│      User       │    │     Roadmap     │    │    Progress     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • id            │    │ • id            │    │ • id            │
│ • username      │    │ • user_id       │    │ • user_id       │
│ • email         │    │ • title         │    │ • roadmap_id    │
│ • learning_goals│    │ • description   │    │ • module_id     │
│ • skill_level   │    │ • modules       │    │ • progress_pct  │
│ • interests     │    │ • learning_goals│    │ • completed     │
│ • email_prefs   │    │ • skill_assess  │    │ • notes         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Educational   │    │   Learning      │    │    Chatbot      │
│     Content     │    │  Environment    │    │   Messages      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • id            │    │ • id            │    │ • id            │
│ • title         │    │ • user_id       │    │ • user_id       │
│ • content_type  │    │ • environment   │    │ • message       │
│ • difficulty    │    │ • preferences   │    │ • response      │
│ • resources     │    │ • settings      │    │ • timestamp     │
│ • tags          │    │ • active        │    │ • context       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🔧 Bileşen Detayları

### 1. Frontend (React + TypeScript)

**Teknolojiler:**
- React 19.1.0
- TypeScript 4.9.5
- Material-UI (MUI) 7.2.0
- React Router DOM 7.7.1
- Axios 1.11.0

**Ana Bileşenler:**

#### 📊 Dashboard
- Kullanıcı genel bakış
- İlerleme özeti
- Hızlı erişim menüleri

#### 🗺️ Roadmap Creator
- Kişiselleştirilmiş roadmap oluşturma
- Modül yönetimi
- İlerleme takibi

#### 💬 Chatbot
- AI destekli sohbet arayüzü
- Öğrenme yardımı
- Soru-cevap sistemi

#### 🎓 Learning Environment
- Öğrenme ortamı ayarları
- Kişiselleştirme seçenekleri
- Tercih yönetimi

#### 🔍 RAG Search
- Gelişmiş arama arayüzü
- Filtreleme seçenekleri
- Sonuç görüntüleme

#### 🤖 Agent Dashboard
- AI agent yönetimi
- Agent durumu izleme
- Görev atama

### 2. Backend (FastAPI + Python)

**Teknolojiler:**
- FastAPI
- Pydantic (veri modelleri)
- Uvicorn (ASGI server)
- Python 3.x

#### 🔐 Authentication Router (`/api/v1/auth`)
```python
# Endpoints:
POST /register          # Kullanıcı kaydı
POST /login            # Kullanıcı girişi
GET  /profile          # Profil bilgileri
PUT  /profile          # Profil güncelleme
```

#### 🗺️ Roadmap Router (`/api/v1/roadmap`)
```python
# Endpoints:
POST /create           # Roadmap oluşturma
GET  /list             # Roadmap listesi
GET  /{id}             # Roadmap detayı
PUT  /{id}             # Roadmap güncelleme
DELETE /{id}           # Roadmap silme
```

#### 💬 Chatbot Router (`/api/v1/chatbot`)
```python
# Endpoints:
POST /chat             # Sohbet mesajı
GET  /history          # Sohbet geçmişi
POST /clear            # Geçmişi temizleme
```

#### 🤖 Agents Router (`/api/v1/agents`)
```python
# Endpoints:
GET  /list             # Agent listesi
GET  /{name}/status    # Agent durumu
POST /{name}/execute   # Agent çalıştırma
POST /{name}/stop      # Agent durdurma
```

#### 📧 Automation Router (`/api/v1/automation`)
```python
# Endpoints:
POST /start            # Otomasyon başlatma
POST /stop             # Otomasyon durdurma
GET  /status           # Durum kontrolü
POST /test-email       # Test e-postası
POST /send-weekly-reminders    # Haftalık hatırlatıcı
POST /send-progress-reports    # İlerleme raporu
```

#### 🔍 RAG Router (`/api/v1/rag`)
```python
# Endpoints:
POST /search           # Genel arama
POST /search-roadmaps  # Roadmap araması
POST /recommendations  # Öneriler
POST /add-document     # Belge ekleme
GET  /pdf/{id}         # PDF indirme
```

### 3. Service Layer

#### 🤖 AI Service (`ai_service.py`)
- **Görev:** Gemini AI entegrasyonu
- **Fonksiyonlar:**
  - Roadmap oluşturma
  - İçerik önerileri
  - Chatbot yanıtları
  - Öğrenme tavsiyeleri

#### 📧 Email Service (`email_service.py`)
- **Görev:** E-posta gönderimi ve yönetimi
- **Fonksiyonlar:**
  - SMTP entegrasyonu
  - HTML şablon yönetimi
  - Toplu e-posta gönderimi
  - E-posta doğrulama

#### 🔄 Automation Service (`automation_service.py`)
- **Görev:** Otomatik görev yönetimi
- **Fonksiyonlar:**
  - Zamanlanmış görevler
  - Haftalık hatırlatıcılar
  - İlerleme raporları
  - Kullanıcı yönetimi

#### 🎓 Educational Content Service (`educational_content_service.py`)
- **Görev:** Eğitim içeriği yönetimi
- **Fonksiyonlar:**
  - İçerik kategorilendirme
  - Zorluk seviyesi belirleme
  - Kaynak yönetimi
  - İçerik önerileri

#### 🏠 Learning Environment Service (`learning_environment_service.py`)
- **Görev:** Öğrenme ortamı yönetimi
- **Fonksiyonlar:**
  - Ortam tercihleri
  - Kişiselleştirme
  - Ayarlar yönetimi
  - Kullanıcı deneyimi

#### 📊 Progress Service (`progress_service.py`)
- **Görev:** İlerleme takibi
- **Fonksiyonlar:**
  - İlerleme hesaplama
  - Başarı metrikleri
  - Raporlama
  - Hedef takibi

#### 🔍 Serp AI Service (`serp_ai_service.py`)
- **Görev:** Web arama entegrasyonu
- **Fonksiyonlar:**
  - Güncel bilgi arama
  - Kaynak doğrulama
  - İçerik güncelleme
  - Trend analizi

### 4. Agent Layer

#### 🤖 Agent Manager (`agent_manager.py`)
- **Görev:** Tüm AI agent'ları koordine etme
- **Özellikler:**
  - Agent yaşam döngüsü yönetimi
  - Görev yönlendirme
  - Agent iletişimi
  - Performans izleme

#### 🗺️ Roadmap Agent (`roadmap_agent.py`)
- **Görev:** Roadmap oluşturma ve yönetimi
- **Özellikler:**
  - Kişiselleştirilmiş roadmap
  - Modül önerileri
  - İlerleme analizi
  - Hedef optimizasyonu

#### 🔗 LangChain Agent (`langchain_agent.py`)
- **Görev:** Modern AI framework entegrasyonu
- **Özellikler:**
  - LangChain tabanlı işlemler
  - Gelişmiş AI yetenekleri
  - Tool kullanımı
  - Chain yönetimi

### 5. RAG System

#### 🔍 Search Service (`search_service.py`)
- **Görev:** Gelişmiş arama ve bilgi çağırma
- **Özellikler:**
  - Semantik arama
  - Filtreleme
  - Skorlama
  - Bağlam çıkarımı

#### 💡 Recommendation Service (`recommendation_service.py`)
- **Görev:** Kişiselleştirilmiş öneriler
- **Özellikler:**
  - Öğrenme tavsiyeleri
  - Sonraki adım önerileri
  - İlgili içerik
  - Günlük tavsiyeler

#### 📄 PDF Generator (`pdf_generator.py`)
- **Görev:** PDF rapor oluşturma
- **Özellikler:**
  - Roadmap PDF'leri
  - İlerleme raporları
  - Öğrenme özetleri
  - Özelleştirilebilir stiller

---

## 🔄 Veri Akışı

### 1. Kullanıcı Kayıt ve Giriş Akışı

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Auth      │    │   User      │    │   Email     │
│   (React)   │    │   Router    │    │   Service   │    │   Service   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ POST /register    │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ Validate Input    │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ Create User       │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ Send Welcome Email│
       │                   │                   │◀──────────────────│
       │                   │                   │                   │
       │                   │ Return Token      │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

### 2. Roadmap Oluşturma Akışı

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │  Roadmap    │    │     AI      │    │  Roadmap    │
│   (React)   │    │   Router    │    │  Service    │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ POST /create      │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ Generate Roadmap  │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ AI Processing     │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ Return Roadmap    │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ Return Roadmap    │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

### 3. Chatbot Sohbet Akışı

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │  Chatbot    │    │     AI      │    │     RAG     │
│   (React)   │    │   Router    │    │  Service    │    │   System    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ POST /chat        │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ Process Message   │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ Search Context    │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ Return Context    │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │                   │ Generate Response │                   │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ Return Response   │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

---

## 🛠️ Teknik Detaylar

### 1. Güvenlik
- **JWT Token Authentication**
- **Password Hashing**
- **CORS Configuration**
- **Input Validation**
- **Rate Limiting**

### 2. Performans
- **Async/Await Pattern**
- **Connection Pooling**
- **Caching Strategy**
- **Lazy Loading**
- **Optimized Queries**

### 3. Ölçeklenebilirlik
- **Microservice Architecture**
- **Load Balancing Ready**
- **Horizontal Scaling**
- **Database Sharding**
- **CDN Integration**

### 4. Monitoring
- **Health Checks**
- **Error Logging**
- **Performance Metrics**
- **User Analytics**
- **System Alerts**

---

## 🚀 Deployment

### Backend Deployment
```bash
# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Docker
docker build -t mywisepath-backend .
docker run -p 8000:8000 mywisepath-backend
```

### Frontend Deployment
```bash
# Build
npm run build

# Serve
npx serve -s build -l 3000

# Docker
docker build -t mywisepath-frontend .
docker run -p 3000:3000 mywisepath-frontend
```

---

## 📈 Gelecek Geliştirmeler

### 1. Kısa Vadeli (1-3 ay)
- [ ] Real-time notifications
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

### 2. Orta Vadeli (3-6 ay)
- [ ] Social learning features
- [ ] Gamification elements
- [ ] Advanced AI models
- [ ] Integration APIs

### 3. Uzun Vadeli (6+ ay)
- [ ] VR/AR learning experiences
- [ ] Blockchain credentials
- [ ] Global marketplace
- [ ] Enterprise solutions

---

## 📊 Proje İstatistikleri

- **Backend:** 15+ servis, 8 router, 6 model
- **Frontend:** 15+ component, 8 sayfa, 6 servis
- **AI Agents:** 3 agent türü, 1 manager
- **RAG System:** 4 ana bileşen
- **API Endpoints:** 50+ endpoint
- **Test Coverage:** 80%+

---

Bu dokümantasyon, MyWisePath projesinin kapsamlı bir özetini sunmaktadır. Proje, modern web teknolojileri ve AI entegrasyonu ile kişiselleştirilmiş öğrenme deneyimi sağlamayı hedeflemektedir.
