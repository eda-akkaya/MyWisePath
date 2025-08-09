# Serp AI Entegrasyonu - MyWisePath

Bu dokümantasyon, MyWisePath platformuna entegre edilen Serp AI özelliklerini açıklar.

## 🎯 Özellikler

### 1. Otomatik Kavram Çıkarma
- LLM kullanıcının chatbot'a girdiği mesajdan öğrenme kavramlarını otomatik olarak çıkarır
- Programlama dilleri, teknolojiler ve öğrenme alanlarını tanır
- Örnek: "Python öğrenmek istiyorum" → `["python", "programlama"]`

### 2. Gerçek Zamanlı Eğitim İçeriği Arama
- Serp AI kullanarak Google'da eğitim içerikleri arar
- Eğitim platformlarını (Coursera, Udemy, YouTube vb.) öncelikler
- Güncel ve kaliteli eğitim kaynakları bulur

### 3. Trend Eğitim Konuları
- Şu anda popüler olan eğitim konularını listeler
- Kullanıcılara güncel öğrenme fırsatları sunar

### 4. AI ile Entegre Analiz
- Gemini AI ile Serp AI'ı birleştirir
- Kullanıcı mesajlarını analiz eder ve uygun eğitim kaynakları önerir

## 🚀 Kurulum

### 1. Gereksinimler
```bash
# Backend requirements'a eklenen paket
google-search-results
```

### 2. Environment Variables
`.env` dosyasına ekleyin:
```env
# Serp AI API Configuration
SERP_API_KEY=your_serp_api_key_here
```

### 3. Serp AI API Key Alma
1. [Serp AI](https://serpapi.com/) sitesine gidin
2. Ücretsiz hesap oluşturun
3. API key'inizi alın
4. `.env` dosyasına ekleyin

## 📁 Dosya Yapısı

```
backend/
├── services/
│   ├── serp_ai_service.py      # Serp AI servis sınıfı
│   └── ai_service.py           # Güncellenmiş AI servis
├── routers/
│   └── chatbot.py              # Güncellenmiş chatbot router
└── config.py                   # SERP_API_KEY eklendi

frontend/
├── src/
│   ├── services/
│   │   └── chatbotService.ts   # Serp AI metodları eklendi
│   └── components/
│       └── Chatbot.tsx         # Serp AI UI entegrasyonu
```

## 🔧 API Endpoints

### Yeni Endpoints

#### 1. Serp AI ile Arama
```http
POST /api/v1/chatbot/search-with-serp
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "Python öğrenmek istiyorum"
}
```

**Response:**
```json
{
  "query": "Python öğrenmek istiyorum",
  "extracted_concepts": ["python", "programlama"],
  "results": [
    {
      "title": "Python Tutorial for Beginners",
      "url": "https://example.com/python-tutorial",
      "snippet": "Learn Python programming...",
      "platform": "YouTube",
      "type": "video",
      "skill_level": "beginner",
      "source": "serp_ai"
    }
  ],
  "total_count": 10,
  "timestamp": "2024-01-01T12:00:00Z",
  "serp_ai_generated": true
}
```

#### 2. Trend Konular
```http
GET /api/v1/chatbot/trending-educational-topics
Authorization: Bearer <token>
```

#### 3. Kavram Çıkarma
```http
POST /api/v1/chatbot/extract-concepts
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "React ve JavaScript öğrenmek istiyorum"
}
```

### Güncellenmiş Endpoints

#### Chatbot Query (Geliştirildi)
```http
POST /api/v1/chatbot/query
```

Artık şu özellikleri içerir:
- Otomatik kavram çıkarma
- Serp AI ile gerçek zamanlı arama
- Güncel eğitim kaynakları önerisi

## 🎨 Frontend Özellikleri

### Yeni UI Bileşenleri

#### 1. Web'de Ara Butonu
- Kullanıcılar doğrudan web'de eğitim içeriği arayabilir
- Serp AI sonuçları güzel kartlar halinde gösterilir

#### 2. Trend Konular Butonu
- Güncel trend eğitim konularını listeler
- Kullanıcılara yeni öğrenme fırsatları sunar

#### 3. Geliştirilmiş Mesaj Görüntüleme
- Serp AI sonuçları özel kartlarda gösterilir
- Platform, tür ve seviye bilgileri
- Direkt linkler ile kolay erişim

### Örnek Kullanım

```typescript
// Serp AI ile arama
const response = await chatbotService.searchWithSerp("Python tutorial");
console.log(response.extracted_concepts); // ["python", "tutorial"]
console.log(response.results); // Eğitim kaynakları

// Trend konular
const trending = await chatbotService.getTrendingEducationalTopics();
console.log(trending.trending_topics); // Popüler konular

// Kavram çıkarma
const concepts = await chatbotService.extractLearningConcepts("React öğrenmek istiyorum");
console.log(concepts.extracted_concepts); // ["react", "programlama"]
```

## 🧪 Test

### Test Script'i Çalıştırma
```bash
cd backend
python ../test_serp_ai.py
```

### Manuel Test
1. Backend'i başlatın: `uvicorn main:app --reload`
2. Frontend'i başlatın: `npm start`
3. Chatbot'u açın
4. "Python öğrenmek istiyorum" yazın
5. Serp AI sonuçlarını kontrol edin

## 🔍 Kavram Çıkarma Algoritması

### Desteklenen Kavramlar

#### Programlama Dilleri
- Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust
- Swift, Kotlin, Dart, TypeScript, Scala, R, MATLAB

#### Teknolojiler ve Framework'ler
- React, Vue, Angular, Node.js, Django, Flask, Spring
- Express, Laravel, ASP.NET, TensorFlow, PyTorch, Scikit-learn
- Pandas, NumPy, Matplotlib, Seaborn, Docker, Kubernetes
- AWS, Azure, GCP, Git, GitHub, SQL, MongoDB, Redis

#### Öğrenme Alanları
- Programlama, Web Geliştirme, Mobil Geliştirme
- Veri Bilimi, Makine Öğrenmesi, Yapay Zeka
- DevOps, Cybersecurity, Blockchain, Game Development
- UI/UX, Database

### Örnek Çıktılar

```python
# Test mesajı: "Python ve React öğrenmek istiyorum"
# Çıktı: ["python", "react", "programlama", "web geliştirme"]

# Test mesajı: "Makine öğrenmesi ve veri bilimi"
# Çıktı: ["makine öğrenmesi", "veri bilimi", "yapay zeka"]

# Test mesajı: "Sadece merhaba"
# Çıktı: ["programlama"] (varsayılan)
```

## 🎯 Kullanım Senaryoları

### Senaryo 1: Yeni Başlayan Öğrenci
1. Kullanıcı: "Programlama öğrenmek istiyorum"
2. Sistem: Kavramları çıkarır → `["programlama"]`
3. Serp AI: Python tutorial'ları arar
4. Sonuç: Güncel Python eğitim kaynakları + yol haritası önerisi

### Senaryo 2: Belirli Teknoloji Öğrenme
1. Kullanıcı: "React ve TypeScript öğrenmek istiyorum"
2. Sistem: Kavramları çıkarır → `["react", "typescript", "web geliştirme"]`
3. Serp AI: React ve TypeScript eğitimleri arar
4. Sonuç: Güncel React/TypeScript kaynakları + seviye bazlı öneriler

### Senaryo 3: Trend Konuları Keşfetme
1. Kullanıcı: "Trend konular" butonuna tıklar
2. Sistem: Güncel popüler eğitim konularını listeler
3. Sonuç: 2024'ün popüler teknolojileri ve eğitim kaynakları

## 🔧 Konfigürasyon

### Serp AI Ayarları
```python
# backend/services/serp_ai_service.py
class SerpAIService:
    def __init__(self):
        self.api_key = SERP_API_KEY
        # Arama parametreleri
        self.search_params = {
            "engine": "google",
            "gl": "tr",  # Türkiye
            "hl": "tr",  # Türkçe
            "safe": "active"
        }
```

### Eğitim Platformları
```python
# Desteklenen platformlar
educational_domains = [
    "coursera.org", "udemy.com", "edx.org", "khanacademy.org",
    "freecodecamp.org", "w3schools.com", "mdn.web", "github.com",
    "youtube.com", "stackoverflow.com", "geeksforgeeks.org",
    "tutorialspoint.com", "programiz.com", "realpython.com"
]
```

## 🚨 Hata Yönetimi

### API Key Eksikse
- Sistem fallback moduna geçer
- Basit kural tabanlı analiz kullanır
- Kullanıcıya uyarı mesajı gösterir

### Ağ Hatası
- Timeout kontrolü
- Retry mekanizması
- Kullanıcı dostu hata mesajları

## 📈 Performans

### Optimizasyonlar
- Maksimum 3 kavram çıkarma (performans için)
- Maksimum 20 arama sonucu
- Asenkron arama işlemleri
- Sonuç önbellekleme

### Öneriler
- API key'i güvenli şekilde saklayın
- Rate limiting'e dikkat edin
- Düzenli olarak sonuçları güncelleyin

## 🔮 Gelecek Özellikler

### Planlanan Geliştirmeler
1. **Çoklu Dil Desteği**: İngilizce ve Türkçe arama
2. **Kişiselleştirilmiş Öneriler**: Kullanıcı geçmişine göre
3. **Gelişmiş Filtreleme**: Seviye, süre, ücret bazlı
4. **Offline Mod**: API olmadığında çalışma
5. **Analytics**: Hangi kaynakların daha popüler olduğu

### Entegrasyon Fırsatları
- YouTube API ile video önerileri
- GitHub API ile kod örnekleri
- Stack Overflow API ile soru-cevap
- LinkedIn Learning entegrasyonu

## 📞 Destek

### Sorun Giderme
1. API key'in doğru olduğunu kontrol edin
2. Network bağlantısını test edin
3. Backend loglarını kontrol edin
4. Test script'ini çalıştırın

### İletişim
- GitHub Issues kullanın
- Detaylı hata mesajları ekleyin
- Test senaryolarını paylaşın

---

**Not**: Bu entegrasyon, kullanıcıların öğrenme deneyimini zenginleştirmek için tasarlanmıştır. Serp AI API kullanımı için lisans koşullarına uygun hareket edin. 