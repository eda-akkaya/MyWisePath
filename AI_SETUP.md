# MyWisePath AI Setup Guide

## 🚀 AI Özelliklerini Etkinleştirme

MyWisePath platformu, Google Gemini AI kullanarak kişiselleştirilmiş öğrenme yol haritaları oluşturur. AI özelliklerini kullanmak için aşağıdaki adımları takip edin:

### 1. Google Gemini API Key Alma

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. API key'inizi kopyalayın

### 2. Environment Dosyası Oluşturma

Backend klasöründe `.env` dosyası oluşturun:

```bash
cd backend
```

`.env` dosyası içeriği:
```env
# Google Gemini AI API Key
GEMINI_API_KEY=your_actual_api_key_here

# JWT Configuration
JWT_SECRET_KEY=mywisepath-secret-key-2024
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration (for future use)
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=mywisepath
```

### 3. Backend'i Başlatma

```bash
cd backend
python main.py
```

Backend varsayılan olarak `http://localhost:8001` adresinde çalışacaktır.

### 4. AI Özelliklerini Test Etme

Test script'ini çalıştırarak AI özelliklerini test edebilirsiniz:

```bash
python test_roadmap.py
```

## 🔧 AI Özellikleri

### Roadmap Generation
- Kullanıcının ilgi alanlarına göre kişiselleştirilmiş yol haritaları
- AI destekli modül önerileri
- Dinamik içerik önerileri

### Chatbot
- AI destekli öğrenme rehberliği
- Akıllı soru-cevap sistemi
- Öğrenme isteklerini analiz etme

### Educational Content
- AI destekli eğitim kaynağı önerileri
- Platform ve kurs önerileri
- Seviyeye uygun içerik filtreleme

## 🛠️ Fallback Sistemi

API key olmadığında veya AI servisi çalışmadığında, sistem otomatik olarak fallback moduna geçer:

- Basit kural tabanlı roadmap oluşturma
- Önceden tanımlanmış içerik önerileri
- Temel chatbot cevapları

## 📊 Test Senaryoları

Test script'i şu senaryoları test eder:

1. **Python Programming**: Python öğrenme yol haritası
2. **Web Development**: Web geliştirme yol haritası
3. **Data Science**: Veri bilimi yol haritası
4. **Machine Learning**: Makine öğrenmesi yol haritası

## 🔍 Troubleshooting

### API Key Hatası
```
Gemini API key ayarlanmamış, fallback cevap döndürülüyor
```
**Çözüm**: `.env` dosyasında doğru API key'in olduğundan emin olun.

### Bağlantı Hatası
```
Bağlantı hatası: Backend çalışmıyor olabilir
```
**Çözüm**: Backend'in `python main.py` ile çalıştığından emin olun.

### Port Hatası
```
[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```
**Çözüm**: Port 8000 kullanımdaysa, `main.py` dosyasında port numarasını değiştirin.

## 📈 Performans

- AI roadmap generation: ~2-3 saniye
- Fallback roadmap generation: ~0.1 saniye
- Chatbot response: ~1-2 saniye

## 🔐 Güvenlik

- API key'ler `.env` dosyasında saklanır
- Production'da environment variables kullanın
- API key'leri asla kod içinde hardcode etmeyin 