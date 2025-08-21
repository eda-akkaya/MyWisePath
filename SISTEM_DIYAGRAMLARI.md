# MyWisePath Sistem Diyagramları ve Çalışma Prensipleri

## 🔄 Sistem Çalışma Akışları

### 1. Kullanıcı Kayıt ve Giriş Süreci

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Auth      │    │   User      │    │   Email     │
│   (React)   │    │   Router    │    │   Service   │    │   Service   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Register Form  │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Validate Input │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ 3. Hash Password  │
       │                   │                   │ & Create User     │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ 4. Send Welcome   │
       │                   │                   │ Email             │
       │                   │                   │◀──────────────────│
       │                   │                   │                   │
       │                   │ 5. Generate JWT   │                   │
       │                   │ Token             │                   │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ 6. Return Token   │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

**Nasıl Çalışır:**
1. **Frontend:** Kullanıcı kayıt formunu doldurur
2. **Auth Router:** Gelen verileri doğrular (email formatı, şifre gücü)
3. **User Service:** Şifreyi hash'ler ve kullanıcıyı oluşturur
4. **Email Service:** Hoş geldin e-postası gönderir
5. **Auth Router:** JWT token oluşturur
6. **Frontend:** Token'ı alır ve kullanıcıyı giriş yapmış olarak işaretler

### 2. Roadmap Oluşturma Süreci

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │  Roadmap    │    │     AI      │    │  Roadmap    │
│   (React)   │    │   Router    │    │  Service    │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Roadmap Form   │                   │                   │
       │ (skills, goals)   │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Validate &     │                   │
       │                   │ Prepare Request   │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ 3. Call Gemini AI │
       │                   │                   │ with Context      │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ 4. AI Generates   │
       │                   │                   │ Roadmap Structure │
       │                   │                   │◀──────────────────│
       │                   │                   │                   │
       │                   │ 5. Process &      │                   │
       │                   │ Structure Data    │                   │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ 6. Return         │                   │                   │
       │ Roadmap Data      │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

**Nasıl Çalışır:**
1. **Frontend:** Kullanıcı beceriler, hedefler ve tercihleri girer
2. **Roadmap Router:** Verileri doğrular ve AI servisine uygun formatta gönderir
3. **AI Service:** Gemini AI'ya kullanıcı bilgilerini ve roadmap şablonunu gönderir
4. **Roadmap Agent:** AI yanıtını işler ve yapılandırılmış roadmap oluşturur
5. **Roadmap Router:** Veriyi frontend'e uygun formatta döndürür
6. **Frontend:** Roadmap'i görsel olarak sunar

### 3. Chatbot Sohbet Süreci

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │  Chatbot    │    │     AI      │    │     RAG     │
│   (React)   │    │   Router    │    │  Service    │    │   System    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. User Message   │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Process &      │                   │
       │                   │ Store Message     │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ 3. Search Relevant│
       │                   │                   │ Context           │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ 4. Return Context │
       │                   │                   │◀──────────────────│
       │                   │                   │                   │
       │                   │ 5. Generate AI    │                   │
       │                   │ Response          │                   │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ 6. Return         │                   │                   │
       │ AI Response       │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

**Nasıl Çalışır:**
1. **Frontend:** Kullanıcı mesajını gönderir
2. **Chatbot Router:** Mesajı işler ve geçmişe kaydeder
3. **AI Service:** RAG sisteminden ilgili bağlamı arar
4. **RAG System:** Kullanıcı sorusuyla ilgili bilgileri bulur
5. **AI Service:** Bağlam ve kullanıcı mesajını birleştirerek yanıt oluşturur
6. **Frontend:** AI yanıtını kullanıcıya gösterir

### 4. E-posta Otomasyon Süreci

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Automation  │    │ Automation  │    │   Email     │    │   Progress  │
│  Scheduler  │    │   Service   │    │   Service   │    │   Service   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Weekly Timer   │                   │                   │
       │ (Monday 09:00)    │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ 2. Get User List  │                   │
       │                   │ & Preferences     │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ 3. Generate       │
       │                   │                   │ Progress Data     │
       │                   │                   │◀──────────────────│
       │                   │                   │                   │
       │                   │ 4. Create Email   │                   │
       │                   │ Content           │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │ 5. Send Emails    │                   │
       │                   │ to All Users      │                   │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ 6. Log Results    │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

**Nasıl Çalışır:**
1. **Scheduler:** Zamanlanmış görevleri kontrol eder
2. **Automation Service:** E-posta gönderimi gereken kullanıcıları belirler
3. **Progress Service:** Her kullanıcı için ilerleme verilerini hesaplar
4. **Email Service:** Kişiselleştirilmiş e-posta içeriği oluşturur
5. **Email Service:** SMTP üzerinden e-postaları gönderir
6. **Automation Service:** Sonuçları loglar

---

## 🏗️ Bileşen İç Yapıları

### 1. AI Service İç Yapısı

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI SERVICE                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Gemini    │  │   Prompt    │  │   Context   │  │ Response│ │
│  │   Client    │  │  Manager    │  │  Builder    │  │ Parser  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Error     │  │   Rate      │  │   Cache     │  │   Log   │ │
│  │  Handler    │  │  Limiter    │  │  Manager    │  │ Manager │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Çalışma Prensibi:**
- **Gemini Client:** Google'ın Gemini AI API'si ile iletişim kurar
- **Prompt Manager:** Farklı görevler için özelleştirilmiş prompt'lar yönetir
- **Context Builder:** Kullanıcı bilgilerini AI'ya uygun formatta hazırlar
- **Response Parser:** AI yanıtlarını yapılandırılmış veriye dönüştürür
- **Error Handler:** API hatalarını yakalar ve uygun yanıtlar döner
- **Rate Limiter:** API çağrılarını sınırlar
- **Cache Manager:** Sık kullanılan yanıtları önbelleğe alır
- **Log Manager:** Tüm AI etkileşimlerini loglar

### 2. RAG System İç Yapısı

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG SYSTEM                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ Document    │  │   Vector    │  │   Search    │  │Recommend│ │
│  │ Processor   │  │   Store     │  │  Engine     │  │ Engine  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Embedding │  │   Chunking  │  │   Scoring   │  │   PDF   │ │
│  │   Model     │  │  Strategy   │  │  Algorithm  │  │Generator│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Çalışma Prensibi:**
- **Document Processor:** PDF, HTML ve metin dosyalarını işler
- **Vector Store:** ChromaDB ile vektör verilerini saklar
- **Search Engine:** Semantik arama yapar
- **Recommend Engine:** Kişiselleştirilmiş öneriler üretir
- **Embedding Model:** Metinleri vektörlere dönüştürür
- **Chunking Strategy:** Büyük metinleri küçük parçalara böler
- **Scoring Algorithm:** Arama sonuçlarını puanlar
- **PDF Generator:** Raporları PDF formatında oluşturur

### 3. Agent Manager İç Yapısı

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT MANAGER                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Agent     │  │   Task      │  │   Agent     │  │   Agent │ │
│  │  Registry   │  │  Queue      │  │  Lifecycle  │  │  Stats  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Task      │  │   Agent     │  │   Error     │  │   Log   │ │
│  │  Router     │  │  Monitor    │  │  Handler    │  │ Manager │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Çalışma Prensibi:**
- **Agent Registry:** Tüm kayıtlı agent'ları yönetir
- **Task Queue:** Bekleyen görevleri sıraya koyar
- **Agent Lifecycle:** Agent'ların yaşam döngüsünü yönetir
- **Agent Stats:** Agent performans metriklerini toplar
- **Task Router:** Görevleri uygun agent'a yönlendirir
- **Agent Monitor:** Agent durumlarını izler
- **Error Handler:** Agent hatalarını yakalar
- **Log Manager:** Tüm agent aktivitelerini loglar

---

## 🔄 Veri Akış Diyagramları

### 1. Kullanıcı Verisi Akışı

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Auth      │    │   User      │    │   Memory    │
│   (React)   │    │   Router    │    │   Service   │    │   Storage   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ User Data         │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ Validate & Hash   │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ Store User Data   │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ Return User ID    │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ Return Token      │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

### 2. Roadmap Verisi Akışı

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │  Roadmap    │    │     AI      │    │   Memory    │
│   (React)   │    │   Router    │    │  Service    │    │   Storage   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ Roadmap Request   │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ Generate with AI  │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ Store Roadmap     │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ Return Roadmap ID │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ Return Roadmap    │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

### 3. Chatbot Verisi Akışı

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │  Chatbot    │    │     AI      │    │   Memory    │
│   (React)   │    │   Router    │    │  Service    │    │   Storage   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ Chat Message      │                   │                   │
       │──────────────────▶│                   │                   │
       │                   │                   │                   │
       │                   │ Process & Store   │                   │
       │                   │──────────────────▶│                   │
       │                   │                   │                   │
       │                   │                   │ Store Message     │
       │                   │                   │──────────────────▶│
       │                   │                   │                   │
       │                   │                   │ Return Message ID │
       │                   │◀──────────────────│                   │
       │                   │                   │                   │
       │ Return Response   │                   │                   │
       │◀──────────────────│                   │                   │
       │                   │                   │                   │
```

---

## 🎯 Bileşenlerin Görevleri ve Nasıl Yaptıkları

### 1. Frontend Bileşenleri

#### Dashboard Component
**Görev:** Kullanıcıya genel bakış sunmak
**Nasıl Yapar:**
- Kullanıcı verilerini API'den çeker
- İlerleme istatistiklerini hesaplar
- Görsel grafikler oluşturur
- Hızlı erişim menüleri sunar

#### RoadmapCreator Component
**Görev:** Kişiselleştirilmiş roadmap oluşturmak
**Nasıl Yapar:**
- Form validasyonu yapar
- AI servisine istek gönderir
- Roadmap verilerini görselleştirir
- İnteraktif modül yönetimi sağlar

#### Chatbot Component
**Görev:** AI destekli sohbet arayüzü
**Nasıl Yapar:**
- Real-time mesaj gönderimi
- Mesaj geçmişini yönetir
- AI yanıtlarını formatlar
- Kullanıcı deneyimini optimize eder

### 2. Backend Servisleri

#### AI Service
**Görev:** Yapay zeka entegrasyonu
**Nasıl Yapar:**
- Gemini AI API'si ile iletişim kurar
- Prompt engineering uygular
- Yanıtları yapılandırılmış formata dönüştürür
- Hata yönetimi ve retry mekanizması

#### Email Service
**Görev:** E-posta gönderimi
**Nasıl Yapar:**
- SMTP protokolü kullanır
- HTML şablonları render eder
- Toplu e-posta gönderimi
- E-posta doğrulama ve tracking

#### Progress Service
**Görev:** İlerleme takibi
**Nasıl Yapar:**
- Kullanıcı aktivitelerini analiz eder
- Başarı metriklerini hesaplar
- Raporlar oluşturur
- Hedef bazlı öneriler sunar

### 3. AI Agent'ları

#### Roadmap Agent
**Görev:** Roadmap oluşturma ve yönetimi
**Nasıl Yapar:**
- Kullanıcı hedeflerini analiz eder
- AI ile kişiselleştirilmiş roadmap üretir
- Modül sıralamasını optimize eder
- İlerleme önerileri sunar

#### LangChain Agent
**Görev:** Modern AI framework entegrasyonu
**Nasıl Yapar:**
- LangChain tools kullanır
- Chain yapıları oluşturur
- Gelişmiş AI yetenekleri sağlar
- Tool kullanımını optimize eder

### 4. RAG Sistemi

#### Search Service
**Görev:** Gelişmiş arama
**Nasıl Yapar:**
- Semantik embedding oluşturur
- Vector similarity search yapar
- Filtreleme ve skorlama uygular
- Bağlam çıkarımı yapar

#### Recommendation Service
**Görev:** Kişiselleştirilmiş öneriler
**Nasıl Yapar:**
- Kullanıcı profili analiz eder
- Collaborative filtering uygular
- Content-based filtering kullanır
- Öneri skorlarını hesaplar

---

## 🔧 Teknik Detaylar

### 1. Güvenlik Mekanizmaları
- **JWT Token:** Stateless authentication
- **Password Hashing:** bcrypt ile güvenli hash
- **CORS:** Cross-origin request kontrolü
- **Input Validation:** Pydantic ile veri doğrulama
- **Rate Limiting:** API çağrı sınırlaması

### 2. Performans Optimizasyonları
- **Async/Await:** Non-blocking I/O operasyonları
- **Caching:** Redis ile önbellekleme
- **Connection Pooling:** Veritabanı bağlantı optimizasyonu
- **Lazy Loading:** Gereksiz veri yüklemeyi önleme
- **Pagination:** Büyük veri setlerini sayfalama

### 3. Ölçeklenebilirlik
- **Microservices:** Bağımsız servis mimarisi
- **Load Balancing:** Yük dengeleme hazırlığı
- **Horizontal Scaling:** Yatay ölçeklendirme
- **Database Sharding:** Veritabanı parçalama
- **CDN Integration:** İçerik dağıtım ağı

Bu diyagramlar ve açıklamalar, MyWisePath projesinin karmaşık yapısını ve bileşenlerin nasıl çalıştığını detaylı bir şekilde göstermektedir.
