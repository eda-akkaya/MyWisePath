# MyWisePath - Kişiselleştirilmiş Öğrenme Platformu

<div align="center">

![MyWisePath Logo](https://img.shields.io/badge/MyWisePath-AI%20Learning%20Platform-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18+-blue?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue?style=for-the-badge&logo=typescript)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi)

**Yapay zeka destekli, kişiselleştirilmiş öğrenme yol haritası platformu**

[🚀 Hızlı Başlangıç](#-hızlı-başlangıç) • [✨ Özellikler](#-özellikler) • [🛠️ Kurulum](#️-kurulum) • [🎯 Demo](#-demo) • [📚 Dokümantasyon](#-dokümantasyon)

</div>

---

## 🎯 Proje Hakkında

MyWisePath, yapay zeka tabanlı, kişiselleştirilmiş bir öğrenme platformudur. Kullanıcıların ilgi alanları, bilgi düzeyleri ve hedefleri doğrultusunda özel öğrenme yol haritaları sunar, ilerlemeyi takip eder ve adaptif içerik önerileri sağlar.

### 🌟 Neden MyWisePath?

- **🤖 AI Destekli**: Google Gemini AI ile akıllı analiz ve öneriler
- **🎯 Kişiselleştirilmiş**: Her kullanıcı için özel öğrenme yol haritası
- **📚 Zengin İçerik**: 6+ eğitim platformundan seçilmiş içerikler
- **🚀 Hızlı Başlangıç**: 5 dakikada kurulum ve kullanıma hazır
- **💻 Modern Teknolojiler**: React, TypeScript, FastAPI ile geliştirildi

## ✨ Özellikler

### 🤖 Yapay Zeka Destekli Öğrenme Asistanı
- **Akıllı Mesaj Analizi**: Kullanıcı isteklerini doğal dil işleme ile analiz eder
- **Otomatik Yol Haritası Oluşturma**: Chatbot üzerinden anında kişiselleştirilmiş yol haritası oluşturur
- **Eğitim İçerik Önerileri**: En iyi eğitim platformlarından seçilmiş içerikler
- **Seviye Belirleme**: Kullanıcının bilgi seviyesini otomatik tespit eder
- **Zaman Planı**: Öğrenme hedeflerine göre gerçekçi zaman planlaması

### 🔐 Kullanıcı Yönetimi
- **Dummy User Simülasyonu**: Test için hazır kullanıcı bilgileri
- **JWT Token Authentication**: Güvenli oturum yönetimi
- **Kullanıcı Profili**: Kişiselleştirilmiş bilgiler ve hedefler
- **Oturum Yönetimi**: Güvenli giriş/çıkış işlemleri

### 🗺️ Yol Haritası Sistemi
- **Kişiselleştirilmiş Roadmap**: Kullanıcı bilgilerine göre özel yol haritası
- **Adım Adım Form**: Bilgi seviyesi, ilgi alanları, hedefler ve zaman planı
- **Modül Bazlı İlerleme**: Her modül için detaylı bilgi ve tahmini süre
- **Görsel İlerleme**: Progress bar ve tamamlanma durumu
- **Eğitim İçerik Entegrasyonu**: Her modül için önerilen eğitim kaynakları
- **İnteraktif Modüller**: Tıklanabilir modül kartları ve detay görünümü

### 📚 Eğitim İçerik Yönetimi
- **Çoklu Platform Desteği**: Coursera, Udemy, freeCodeCamp, YouTube, edX, Khan Academy
- **Seviye Bazlı Öneriler**: Başlangıç, orta, ileri seviye içerikler
- **Ücretsiz/Ücretli Filtreleme**: Bütçeye uygun içerik önerileri
- **İnteraktif İçerik Kartları**: Görsel ve kullanıcı dostu arayüz
- **Detaylı İçerik Bilgileri**: Süre, seviye, platform, ücret bilgileri

### 🎨 Modern Arayüz
- **Material UI v7**: Modern ve responsive tasarım
- **Stepper Navigation**: Adım adım form gezinmesi
- **Interactive Components**: Chip seçimleri, form validasyonu
- **Responsive Design**: Mobil ve desktop uyumlu
- **Chatbot Arayüzü**: Floating chat butonu ile kolay erişim
- **Dark/Light Mode**: Tema desteği (gelecek özellik)

## 🚀 Hızlı Başlangıç

### ⚡ 5 Dakikada Kurulum

```bash
# 1. Repository'yi klonlayın
git clone https://github.com/yourusername/MyWisePath.git
cd MyWisePath

# 2. Backend'i başlatın
cd backend
pip install -r requirements.txt
python main.py

# 3. Yeni terminal açın ve frontend'i başlatın
cd frontend
npm install
npm start
```

### 🔑 Demo Giriş Bilgileri
- **Email**: `demo@mywisepath.com`
- **Şifre**: `demo123`

### 🎯 Hızlı Test
1. `http://localhost:3000` adresine gidin
2. Demo bilgileri ile giriş yapın
3. Chatbot'u açın ve "Python öğrenmek istiyorum" yazın
4. AI'nın önerdiği yol haritasını inceleyin

## 🛠️ Kurulum

### Gereksinimler

| Teknoloji | Minimum Versiyon | Önerilen Versiyon |
|-----------|------------------|-------------------|
| Node.js   | v16.0.0         | v18.0.0+         |
| Python    | v3.8.0          | v3.11.0+         |
| npm       | v8.0.0          | v9.0.0+          |
| pip       | v21.0.0         | v23.0.0+         |

### 🔧 Ortam Kurulumu

#### Windows
```bash
# Node.js kurulumu (Chocolatey ile)
choco install nodejs

# Python kurulumu
winget install Python.Python.3.11
```

#### macOS
```bash
# Homebrew ile kurulum
brew install node python@3.11

# pip güncelleme
python3 -m pip install --upgrade pip
```

#### Linux (Ubuntu/Debian)
```bash
# Node.js kurulumu
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python kurulumu
sudo apt update
sudo apt install python3.11 python3-pip
```

### Backend Kurulumu

```bash
cd backend

# Sanal ortam oluşturma (önerilen)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate     # Windows

# Bağımlılıkları yükleme
pip install -r requirements.txt

# Uygulamayı başlatma
python main.py
```

**Backend URL**: `http://localhost:8000`
**API Dokümantasyonu**: `http://localhost:8000/docs`

### Frontend Kurulumu

```bash
cd frontend

# Bağımlılıkları yükleme
npm install

# Geliştirme sunucusunu başlatma
npm start
```

**Frontend URL**: `http://localhost:3000`

### 🔐 Ortam Değişkenleri

Backend için `.env` dosyası oluşturun:

```bash
cd backend
cp env_example.txt .env
```

`.env` dosyasını düzenleyin:

```env
# AI API Key (Google Gemini)
GEMINI_API_KEY=your_gemini_api_key_here

# JWT Secret
JWT_SECRET=your_jwt_secret_here

# Database URL (gelecek özellik)
DATABASE_URL=mongodb://localhost:27017/mywisepath

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 🎯 Demo

### 🚀 Demo Sayfası
Demo sayfasını ziyaret ederek tüm özellikleri test edebilirsiniz:
- **URL**: `http://localhost:3000/demo`
- **Özellikler**: 
  - Yapay zeka destekli yol haritası oluşturma
  - Eğitim içerik önerileri
  - Örnek sorgular ile test
  - Gerçek zamanlı AI analizi

### 💬 Chatbot Demo
1. Sağ alt köşedeki chat butonuna tıklayın
2. Örnek sorgular:
   - "Python öğrenmek istiyorum"
   - "Web geliştirme için yol haritası oluştur"
   - "Veri bilimi öğrenmek istiyorum, başlangıç seviyesindeyim"
   - "3 ayda React öğrenmek istiyorum"

## 📁 Proje Yapısı

```
MyWisePath/
├── 📁 frontend/                 # React.js Frontend
│   ├── 📁 src/
│   │   ├── 📁 components/       # React bileşenleri
│   │   │   ├── 🤖 Chatbot.tsx   # AI destekli chatbot
│   │   │   ├── 📚 EducationalContent.tsx # Eğitim içerik bileşeni
│   │   │   └── 🔒 PrivateRoute.tsx
│   │   ├── 📁 contexts/         # Context API
│   │   │   └── 🔐 AuthContext.tsx
│   │   ├── 📁 pages/           # Sayfa bileşenleri
│   │   │   ├── 🎯 Demo.tsx     # Demo sayfası
│   │   │   ├── 🏠 Dashboard.tsx
│   │   │   ├── 🗺️ Roadmap.tsx
│   │   │   ├── 🔐 Login.tsx
│   │   │   └── 📝 Register.tsx
│   │   ├── 📁 services/        # API servisleri
│   │   │   ├── 🤖 chatbotService.ts # Chatbot API
│   │   │   ├── 🗺️ roadmapService.ts # Roadmap API
│   │   │   └── 🔐 authService.ts # Auth API
│   │   ├── 📁 types/           # TypeScript tipleri
│   │   └── 📄 App.tsx          # Ana uygulama
│   ├── 📄 package.json
│   └── 📄 tsconfig.json
├── 📁 backend/                  # FastAPI Backend
│   ├── 📁 routers/             # API router'ları
│   │   ├── 🤖 chatbot.py       # Chatbot ve AI endpoints
│   │   ├── 🗺️ roadmap.py       # Yol haritası endpoints
│   │   └── 🔐 auth.py          # Authentication
│   ├── 📁 services/            # İş mantığı servisleri
│   │   ├── 🤖 ai_service.py    # AI analiz ve cevap servisi
│   │   └── 📚 educational_content_service.py # Eğitim içerik servisi
│   ├── 📁 models/              # Pydantic modelleri
│   │   ├── 📚 educational_content.py # Eğitim içerik modelleri
│   │   ├── 🗺️ roadmap.py       # Roadmap modelleri
│   │   ├── 🤖 chatbot.py       # Chatbot modelleri
│   │   └── 👤 user.py          # Kullanıcı modelleri
│   ├── 📁 utils/               # Yardımcı fonksiyonlar
│   │   ├── 🔐 auth.py          # Authentication utilities
│   │   └── 📋 constants.py     # Sabitler
│   ├── 📄 main.py              # Ana uygulama
│   ├── 📄 config.py            # Konfigürasyon
│   ├── 📄 requirements.txt     # Python bağımlılıkları
│   └── 📄 env_example.txt      # Örnek ortam değişkenleri
├── 📁 shared/                  # Ortak dosyalar
├── 📄 README.md               # Bu dosya
└── 📄 AI_SETUP.md             # AI kurulum rehberi
```

## 🔧 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `POST` | `/api/v1/auth/register` | Kullanıcı kaydı |
| `POST` | `/api/v1/auth/login` | Kullanıcı girişi |
| `GET` | `/api/v1/auth/me` | Mevcut kullanıcı bilgileri |

### 🤖 Chatbot & AI
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `POST` | `/api/v1/chatbot/query` | Chatbot ile sohbet |
| `POST` | `/api/v1/chatbot/generate-roadmap` | Chatbot'tan yol haritası oluştur |
| `GET` | `/api/v1/chatbot/content-recommendations/{topic}` | İçerik önerileri |
| `GET` | `/api/v1/chatbot/welcome` | Karşılama mesajı |

### 🗺️ Roadmap
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `POST` | `/api/v1/roadmap/generate` | Yol haritası oluşturma |
| `POST` | `/api/v1/roadmap/generate-from-chat` | Chat mesajından yol haritası |
| `GET` | `/api/v1/roadmap/content-recommendations/{topic}` | Konu bazlı içerik |
| `GET` | `/api/v1/roadmap/progress/{roadmap_id}` | İlerleme takibi |

## 🎨 Kullanılan Teknolojiler

### Frontend
| Teknoloji | Versiyon | Amaç |
|-----------|----------|------|
| **React.js** | 18.x | UI framework |
| **TypeScript** | 5.x | Tip güvenliği |
| **Material UI** | 7.x | UI component library |
| **React Router** | 6.x | Sayfa yönlendirme |
| **Axios** | 1.x | HTTP client |
| **React Hook Form** | 7.x | Form yönetimi |

### Backend
| Teknoloji | Versiyon | Amaç |
|-----------|----------|------|
| **FastAPI** | 0.100+ | Web framework |
| **Pydantic** | 2.x | Data validation |
| **Python-Jose** | 3.x | JWT token işlemleri |
| **Passlib** | 1.x | Şifre hash'leme |
| **Uvicorn** | 0.20+ | ASGI server |
| **Google Gemini AI** | 1.x | Yapay zeka analizi |

## 🤖 AI Özellikleri

### 🧠 Akıllı Mesaj Analizi
- **Doğal Dil İşleme**: Kullanıcı isteklerini anlama
- **Öğrenme Alanı Tespiti**: Otomatik konu belirleme
- **Seviye Belirleme**: Başlangıç, orta, ileri seviye tespiti
- **Zaman Planı Çıkarımı**: Gerçekçi öğrenme süreleri
- **Hedef Analizi**: Kariyer ve kişisel hedefler

### 🎯 Desteklenen Öğrenme Alanları

#### 💻 Programlama
- **Python**: Django, Flask, FastAPI, Data Science
- **JavaScript**: React, Vue, Angular, Node.js
- **Java**: Spring Boot, Android Development
- **C++/C#**: Game Development, System Programming
- **PHP/Ruby**: Web Development
- **Go/Rust**: System Programming, Microservices

#### 📊 Veri Bilimi & AI
- **Veri Analizi**: Pandas, NumPy, Matplotlib, Seaborn
- **Makine Öğrenmesi**: Scikit-learn, TensorFlow, PyTorch
- **Deep Learning**: Neural Networks, CNN, RNN, Transformers
- **Veri Görselleştirme**: Plotly, D3.js, Tableau
- **Big Data**: Apache Spark, Hadoop, Kafka

#### 🌐 Web Geliştirme
- **Frontend**: HTML, CSS, JavaScript, React, Vue, Angular
- **Backend**: Node.js, Django, Flask, FastAPI, Express
- **Database**: SQL, NoSQL, MongoDB, PostgreSQL
- **DevOps**: Docker, Kubernetes, CI/CD

#### 📱 Mobil Geliştirme
- **Android**: Kotlin, Java, Android Studio
- **iOS**: Swift, Objective-C, Xcode
- **Cross-Platform**: Flutter, React Native, Xamarin

#### ☁️ DevOps & Cloud
- **Containerization**: Docker, Kubernetes
- **Cloud Platforms**: AWS, Azure, Google Cloud
- **CI/CD**: Jenkins, GitHub Actions, GitLab CI
- **Monitoring**: Prometheus, Grafana, ELK Stack

### 📚 Eğitim Platformları
| Platform | Tür | Özellik |
|----------|-----|---------|
| **Coursera** | Ücretli | Üniversite kalitesinde kurslar |
| **Udemy** | Ücretli | Pratik odaklı eğitimler |
| **freeCodeCamp** | Ücretsiz | Interaktif öğrenme |
| **YouTube** | Ücretsiz | Video tabanlı eğitimler |
| **edX** | Ücretli | Akademik kurslar |
| **Khan Academy** | Ücretsiz | Temel konular |

## 📋 Yapılacaklar (Roadmap)

### ✅ Tamamlanan Özellikler
- [x] Temel authentication sistemi
- [x] Login/Register arayüzü
- [x] Dashboard sayfası
- [x] Yol haritası oluşturma formu
- [x] Dummy user simülasyonu
- [x] Modern UI tasarımı
- [x] **Yapay zeka destekli chatbot**
- [x] **Otomatik yol haritası oluşturma**
- [x] **Eğitim içerik önerileri**
- [x] **Demo sayfası**
- [x] **Material UI v7 entegrasyonu**
- [x] **TypeScript desteği**

### 🚧 Geliştirme Aşamasında
- [ ] Gerçek veritabanı entegrasyonu (MongoDB)
- [ ] OpenAI API entegrasyonu (alternatif AI)
- [ ] İlerleme grafikleri ve analitikler
- [ ] Quiz/test sistemi
- [ ] Kullanıcı profil güncelleme

### 🔮 Gelecek Aşamalar
- [ ] Email doğrulama sistemi
- [ ] Şifre sıfırlama
- [ ] Sosyal medya ile giriş
- [ ] Çoklu dil desteği
- [ ] Mobil uygulama (React Native)
- [ ] Gelişmiş AI analizi
- [ ] Gerçek zamanlı içerik önerileri
- [ ] Modül içerik yönetimi
- [ ] Dark/Light tema desteği
- [ ] Offline çalışma modu
- [ ] Gamification (başarı rozetleri)
- [ ] Topluluk özellikleri

## 🎯 Kullanım Örnekleri

### 💬 Chatbot ile Yol Haritası Oluşturma

#### Adım 1: Chatbot'u Açın
- Sağ alt köşedeki chat butonuna tıklayın
- Veya `/demo` sayfasını ziyaret edin

#### Adım 2: Sorgunuzu Yazın
```
"Python öğrenmek istiyorum, veri bilimi alanında çalışmak istiyorum"
```

#### Adım 3: AI Analizi
AI şunları analiz eder:
- **Öğrenme Alanı**: Python, Veri Bilimi
- **Seviye**: Başlangıç (varsayılan)
- **Hedef**: Veri Bilimi kariyeri
- **Zaman Planı**: 6-12 ay

#### Adım 4: Yol Haritası Oluşturma
- "Yol Haritası Oluştur" butonuna tıklayın
- Detaylı modüller görüntülenir
- Her modül için eğitim içerikleri önerilir

### 🎯 Demo Sayfası ile Test

#### Örnek Sorgular:
1. **"Web geliştirme öğrenmek istiyorum"**
   - Frontend: HTML, CSS, JavaScript
   - Backend: Node.js, Express
   - Database: MongoDB

2. **"3 ayda React öğrenmek istiyorum"**
   - JavaScript temelleri
   - React fundamentals
   - State management
   - Real-world projects

3. **"Veri bilimi için Python öğrenmek istiyorum"**
   - Python basics
   - Data manipulation (Pandas, NumPy)
   - Data visualization
   - Machine Learning basics

## 🛠️ Geliştirme

### 🔧 Geliştirme Ortamı Kurulumu

```bash
# Backend geliştirme
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Geliştirme bağımlılıkları
python main.py --reload  # Otomatik yeniden başlatma

# Frontend geliştirme
cd frontend
npm install
npm run dev  # Hot reload ile geliştirme
```

### 🧪 Test Çalıştırma

```bash
# Backend testleri
cd backend
python -m pytest

# Frontend testleri
cd frontend
npm test
```

### 📦 Build İşlemleri

```bash
# Frontend production build
cd frontend
npm run build

# Backend production
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🐛 Sorun Giderme

### Yaygın Sorunlar

#### Backend Başlatılamıyor
```bash
# Port 8000 kullanımda
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/macOS

# Farklı port kullanın
python main.py --port 8001
```

#### Frontend Başlatılamıyor
```bash
# Port 3000 kullanımda
netstat -ano | findstr :3000  # Windows
lsof -i :3000                 # Linux/macOS

# Farklı port kullanın
PORT=3001 npm start
```

#### AI API Hatası
```bash
# Gemini API key kontrolü
echo $GEMINI_API_KEY

# .env dosyasını kontrol edin
cat backend/.env
```

#### Bağımlılık Sorunları
```bash
# Python sanal ortamı yeniden oluşturun
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js modüllerini temizleyin
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 📞 Destek

Sorun yaşıyorsanız:
1. [Issues](https://github.com/yourusername/MyWisePath/issues) sayfasını kontrol edin
2. Yeni issue oluşturun
3. Detaylı hata mesajı ve sistem bilgilerini paylaşın

## 🤝 Katkıda Bulunma

MyWisePath'e katkıda bulunmak istiyorsanız:

### 🚀 Hızlı Başlangıç
1. Bu repository'yi fork edin
2. Feature branch oluşturun: `git checkout -b feature/amazing-feature`
3. Değişikliklerinizi commit edin: `git commit -m 'Add some amazing feature'`
4. Branch'inizi push edin: `git push origin feature/amazing-feature`
5. Pull Request oluşturun

### 📋 Katkı Rehberi
- Kod standartlarına uyun (ESLint, Prettier)
- Test yazın
- Dokümantasyonu güncelleyin
- Commit mesajlarını açıklayıcı yazın

### 🎯 Katkı Alanları
- 🐛 Bug düzeltmeleri
- ✨ Yeni özellikler
- 📚 Dokümantasyon iyileştirmeleri
- 🎨 UI/UX iyileştirmeleri
- 🧪 Test yazımı
- 🌐 Çoklu dil desteği

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Google Gemini AI](https://ai.google.dev/) - Yapay zeka desteği
- [Material UI](https://mui.com/) - UI component library
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://reactjs.org/) - Frontend framework

## 📞 İletişim

- **Email**: edaakkaya12@hotmail.com.tr


---

<div align="center">

**MyWisePath** - Geleceğin öğrenme platformu 🚀

[⭐ Star this repo](https://github.com/yourusername/MyWisePath) • [🐛 Report Bug](https://github.com/yourusername/MyWisePath/issues) • [💡 Request Feature](https://github.com/yourusername/MyWisePath/issues)

</div> 
