# MyWisePath - Kişiselleştirilmiş Öğrenme Platformu
English version of this file -> README_EN.md

*Bu projeyi Akbank ve UpSchool tarafından düzenlenen AI First Developer Programı kapsamında öğrendiğim bilgileri ve teknikleri uygulamak için gerçekleştirdim. Tamamen yapay zeka (Cursor Pro) kullanarak yaptım (Programın amacı buydu).*

*PROJE_OZETI.md ve SISTEM_DIYAGRAMLARI.md dosyalarını okuyarak sistemin yapısını kolayca kavrayabilirsiniz.*

MyWisePath, kullanıcıların kişisel öğrenme yolculuklarını planlamalarına ve takip etmelerine yardımcı olan bir platformdur. AI destekli öneriler, interaktif chatbot ve kişiselleştirilmiş roadmap'ler sunar.



## 🚀 Özellikler

- **AI Destekli Öğrenme Önerileri**: Gemini AI ile kişiselleştirilmiş içerik önerileri
- **İnteraktif Chatbot**: Öğrenme sürecinde yardım ve rehberlik
- **Kişiselleştirilmiş Roadmap**: Hedeflerinize uygun öğrenme yolları
- **E-posta Otomasyonu**: Haftalık hatırlatıcılar ve ilerleme raporları
- **Modern Web Arayüzü**: React ile geliştirilmiş kullanıcı dostu arayüz
- **RAG Sistemi**: Gelişmiş arama ve bilgi çağırma sistemi
- **LangChain Agent'ları**: Modern AI framework entegrasyonu
- **Serp AI Entegrasyonu**: Gerçek zamanlı eğitim içeriği arama
- **Parametric System Prompt**: Roadmap tabanlı dinamik AI yanıtları
- **PDF Raporlama**: Roadmap ve ilerleme raporları PDF formatında

## 🔍 RAG (Retrieval-Augmented Generation) Sistemi

### Özellikler:
- **Semantik Arama**: Kullanıcı sorgularını anlayarak ilgili içerikleri bulma
- **Filtreleme**: Kaynak, dosya türü ve içerik türüne göre filtreleme
- **Skorlama**: Benzerlik skorları ile sonuçları sıralama
- **Bağlam Çıkarımı**: Sorgu için ilgili bağlam metinlerini oluşturma
- **Tavsiye Sistemi**: Kişiselleştirilmiş öğrenme önerileri
- **PDF İndirme**: Roadmap ve ilerleme raporları PDF formatında

### API Endpoint'leri:
```
POST /api/v1/rag/upload-document          # Belge yükleme
POST /api/v1/rag/add-roadmap              # Roadmap ekleme
GET  /api/v1/rag/search                   # Genel arama
GET  /api/v1/rag/search-roadmaps          # Roadmap araması
POST /api/v1/rag/recommendations/learning # Öğrenme tavsiyeleri
POST /api/v1/rag/generate-pdf/roadmap     # Roadmap PDF'i
GET  /api/v1/rag/stats                    # Sistem istatistikleri
```

## 🤖 LangChain Agent Sistemi

### Modern AI Framework Entegrasyonu:
- **LangChain Roadmap Agent**: Gelişmiş roadmap oluşturma
- **Tool Integration**: Decorator tabanlı araç entegrasyonu
- **Conversation Memory**: Gelişmiş konuşma belleği
- **Error Handling**: Kapsamlı hata yönetimi
- **Async Support**: Asenkron işlem desteği

### API Endpoint'leri:
```
POST /api/v1/agents/langchain/create-roadmap  # LangChain roadmap oluşturma
GET  /api/v1/agents/status                    # Agent durumu
POST /api/v1/agents/execute-task              # Görev yürütme
```

## 🔍 Serp AI Entegrasyonu

### Gerçek Zamanlı Eğitim İçeriği:
- **Otomatik Kavram Çıkarma**: LLM ile öğrenme kavramlarını tanıma
- **Eğitim Platformları**: Coursera, Udemy, YouTube vb. entegrasyonu
- **Trend Konular**: Güncel popüler eğitim konuları
- **Seviye Bazlı Arama**: Kullanıcı seviyesine uygun içerik

### API Endpoint'leri:
```
POST /api/v1/chatbot/search-with-serp         # Serp AI ile arama
GET  /api/v1/chatbot/trending-educational-topics  # Trend konular
POST /api/v1/chatbot/comprehensive-learning   # Kapsamlı öğrenme
```

## 🎯 Parametric System Prompt

### Roadmap Tabanlı Dinamik Yanıtlar:
- **Seviye Bazlı Kişiselleştirme**: Beginner, Intermediate, Advanced
- **İlgi Alanı Bazlı Özelleştirme**: AI, Web Development, Python vb.
- **Hedef Odaklı Rehberlik**: Kariyer, Proje, Sertifika odaklı
- **Zaman Planı Bazlı Özelleştirme**: Haftalık çalışma saatine göre

### Özellikler:
- Kullanıcının roadmap bilgilerine göre otomatik prompt oluşturma
- Seviye bazlı talimatlar ve öneriler
- İlgi alanlarına özel yönergeler
- Zaman planına uygun öğrenme stratejileri

## 📧 E-posta Otomasyonu

Platform, kullanıcıların öğrenme sürecini desteklemek için otomatik e-posta sistemi içerir:

### Özellikler:
- **Haftalık Hatırlatıcılar**: Her Pazartesi saat 09:00'da gönderilir
- **İlerleme Raporları**: Her Pazar saat 18:00'da gönderilir
- **Kişiselleştirilmiş İçerik**: Kullanıcının hedeflerine göre özelleştirilmiş
- **HTML E-posta Şablonları**: Modern ve responsive tasarım

### API Endpoint'leri:
```
POST /api/v1/automation/start          # Otomasyonu başlat
POST /api/v1/automation/stop           # Otomasyonu durdur
GET  /api/v1/automation/status         # Durumu kontrol et
POST /api/v1/automation/test-email     # Test e-postası gönder
POST /api/v1/automation/send-weekly-reminders    # Manuel haftalık hatırlatıcı
POST /api/v1/automation/send-progress-reports    # Manuel ilerleme raporu
GET  /api/v1/automation/users          # Kullanıcıları listele
POST /api/v1/automation/users          # Yeni kullanıcı ekle
DELETE /api/v1/automation/users/{email} # Kullanıcı kaldır
```

## 🛠️ Kurulum

### Backend Kurulumu

1. **Bağımlılıkları yükleyin:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Environment variables'ları ayarlayın:**
```bash
cp env_example.txt .env
```

`.env` dosyasını düzenleyin:
```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Serp AI Configuration
SERP_API_KEY=your_serp_api_key_here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
EMAIL_FROM=noreply@mywisepath.com
EMAIL_FROM_NAME=MyWisePath

# Email Automation Settings
WEEKLY_REMINDER_ENABLED=true
PROGRESS_REPORT_ENABLED=true

# Vector Store Settings (RAG System)
VECTOR_STORE_TYPE=chroma
VECTOR_STORE_PATH=./vector_store
EMBEDDING_MODEL=huggingface
```

3. **Gerekli dizinleri oluşturun:**
```bash
mkdir -p vector_store pdfs temp
```

4. **Backend'i başlatın:**
```bash
python main.py
```

### Frontend Kurulumu

1. **Bağımlılıkları yükleyin:**
```bash
cd frontend
npm install
```

2. **Frontend'i başlatın:**
```bash
npm start
```

## 🧪 Test

### RAG Sistemi Testi:
```bash
python test_rag_system.py
```

### LangChain Agent Testi:
```bash
python test_langchain_agent.py
```

### Serp AI Testi:
```bash
python test_serp_ai.py
```

### Parametric Prompt Testi:
```bash
python test_parametric_prompt.py
```

### E-posta Otomasyonu Testi:
```bash
python test_email_automation.py
```

## 📁 Proje Yapısı

```
MyWisePath/
├── backend/
│   ├── main.py                    # FastAPI uygulaması
│   ├── config.py                  # Konfigürasyon
│   ├── requirements.txt           # Python bağımlılıkları
│   ├── routers/                   # API router'ları
│   │   ├── auth.py               # Kimlik doğrulama
│   │   ├── roadmap.py            # Roadmap işlemleri
│   │   ├── chatbot.py            # Chatbot API
│   │   ├── automation.py         # E-posta otomasyonu
│   │   ├── agents.py             # Agent yönetimi
│   │   └── rag.py                # RAG sistemi
│   ├── services/                  # İş mantığı servisleri
│   │   ├── ai_service.py         # AI servisleri
│   │   ├── educational_content_service.py  # İçerik servisleri
│   │   ├── email_service.py      # E-posta servisi
│   │   ├── automation_service.py # Otomasyon servisi
│   │   ├── serp_ai_service.py    # Serp AI entegrasyonu
│   │   └── live_content_service.py # Gerçek zamanlı içerik
│   ├── agents/                    # AI Agent'ları
│   │   ├── base_agent.py         # Temel agent sınıfı
│   │   ├── agent_manager.py      # Agent yöneticisi
│   │   ├── roadmap_agent.py      # Roadmap agent'ı
│   │   └── langchain_agent.py    # LangChain agent'ı
│   ├── rag/                       # RAG Sistemi
│   │   ├── document_processor.py # Belge işleme
│   │   ├── vector_store.py       # VectorDB yönetimi
│   │   ├── search_service.py     # Arama servisi
│   │   ├── recommendation_service.py # Tavsiye sistemi
│   │   └── pdf_generator.py      # PDF oluşturma
│   ├── models/                    # Veri modelleri
│   ├── vector_store/              # Vector veritabanı
│   └── pdfs/                      # PDF dosyaları
├── frontend/                      # React uygulaması
│   ├── src/
│   │   ├── components/
│   │   │   ├── RAGSearch.tsx     # RAG arama bileşeni
│   │   │   ├── AgentDashboard.tsx # Agent dashboard
│   │   │   └── PDFGenerator.tsx  # PDF oluşturma
│   │   └── services/
│   │       ├── agentService.ts   # Agent servisleri
│   │       └── ragService.ts     # RAG servisleri
└── test_*.py                     # Test dosyaları
```

## 🔧 E-posta Konfigürasyonu

### Gmail App Password Kullanımı:

1. Google Hesabınızda 2FA'yı etkinleştirin
2. App Passwords bölümünden yeni bir şifre oluşturun
3. Bu şifreyi `SMTP_PASSWORD` olarak kullanın

### SMTP Ayarları:
- **Gmail**: smtp.gmail.com:587
- **Outlook**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587

## 📊 Otomasyon Zamanlaması

- **Haftalık Hatırlatıcılar**: Her Pazartesi 09:00
- **İlerleme Raporları**: Her Pazar 18:00
- **Özel Zamanlama**: API üzerinden özelleştirilebilir

## 🔑 API Key'ler

### Gerekli API Key'ler:
1. **Gemini API Key**: AI servisleri için
2. **Serp API Key**: Gerçek zamanlı arama için

### API Key Alma:
- **Gemini**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Serp AI**: [Serp API](https://serpapi.com/)

## 🚀 Kullanım Örnekleri

### 1. Roadmap Oluşturma
```bash
curl -X POST "http://localhost:8001/api/v1/roadmap/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_level": "intermediate",
    "interests": ["Python", "AI"],
    "learning_goals": ["Machine Learning"],
    "available_hours_per_week": 20,
    "target_timeline_months": 6
  }'
```

### 2. RAG Arama
```bash
curl -X GET "http://localhost:8001/api/v1/rag/search?query=Python%20programlama&k=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Serp AI ile Arama
```bash
curl -X POST "http://localhost:8001/api/v1/chatbot/search-with-serp" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Python öğrenmek istiyorum"}'
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Proje hakkında sorularınız için issue açabilirsiniz. 
