# RAG (Retrieval-Augmented Generation) Sistemi

Bu klasör, MyWisePath platformu için gelişmiş bir RAG sistemi içerir. RAG sistemi, kullanıcılara daha akıllı ve kişiselleştirilmiş öğrenme deneyimi sunmak için tasarlanmıştır.

## 🎯 Sistem Özellikleri

### 1. Basit Bilgi Çağırma (Search) Sistemi
- **Semantik Arama**: Kullanıcı sorgularını anlayarak ilgili içerikleri bulma
- **Filtreleme**: Kaynak, dosya türü ve içerik türüne göre filtreleme
- **Skorlama**: Benzerlik skorları ile sonuçları sıralama
- **Bağlam Çıkarımı**: Sorgu için ilgili bağlam metinlerini oluşturma

### 2. Tavsiye Sistemi
- **Öğrenme Tavsiyeleri**: Kullanıcı ilgi alanlarına göre roadmap önerileri
- **Sonraki Adım Tavsiyeleri**: Mevcut ilerlemeye göre sonraki modül önerileri
- **Kişiselleştirilmiş İçerik**: Kullanıcı profili ve geçmişine göre içerik
- **Günlük Tavsiyeler**: Motivasyon ve keşif için günlük öneriler
- **İlgili İçerik**: Belirli bir içerikle ilgili diğer materyaller

### 3. Chunking Stratejisi
- **PDF İşleme**: PyMuPDF ile PDF dosyalarını metne çevirme
- **Blog İçeriği**: HTML etiketlerini temizleyerek metin çıkarma
- **Roadmap İşleme**: Roadmap verilerini yapılandırılmış metne dönüştürme
- **Akıllı Bölme**: RecursiveCharacterTextSplitter ile optimal chunk boyutları
- **Overlap Yönetimi**: Chunk'lar arası bağlam kaybını önleme

### 4. VectorDB Entegrasyonu
- **Chroma DB**: Yerel vektör veritabanı (varsayılan)
- **FAISS**: Facebook'un hızlı benzerlik arama kütüphanesi
- **Embedding Modelleri**: OpenAI ve HuggingFace entegrasyonu
- **Persistent Storage**: Vektör verilerinin kalıcı saklanması
- **Collection Yönetimi**: Dinamik collection oluşturma ve yönetimi

### 5. PDF İndirme Özelliği
- **Roadmap PDF**: Roadmap'leri profesyonel PDF formatında oluşturma
- **İlerleme Raporu**: Kullanıcı ilerleme verilerini PDF raporu
- **Öğrenme Özeti**: Öğrenme geçmişi ve başarıları PDF özeti
- **Özelleştirilebilir Stiller**: Profesyonel görünüm için özel stiller
- **Otomatik Temizlik**: Eski PDF dosyalarının otomatik silinmesi

## 📁 Dosya Yapısı

```
rag/
├── __init__.py                 # RAG modülü başlatma
├── document_processor.py       # Belge işleme ve chunking
├── vector_store.py            # VectorDB yönetimi
├── search_service.py          # Arama ve bilgi çağırma
├── recommendation_service.py  # Tavsiye sistemi
├── pdf_generator.py           # PDF oluşturma
└── rag-readme.md             # Bu dosya
```

## 🔧 Kurulum ve Yapılandırma

### 1. Gerekli Bağımlılıklar
```bash
pip install langchain langchain-community chromadb faiss-cpu sentence-transformers PyMuPDF reportlab numpy
```

### 2. Environment Variables
```env
# Vector Store Ayarları (Ücretsiz modeller)
VECTOR_STORE_TYPE=chroma  # chroma veya faiss
VECTOR_STORE_PATH=./vector_store
EMBEDDING_MODEL=huggingface  # huggingface, sentence-transformers, instructor
```

### 3. Dizin Yapısı
```bash
mkdir -p vector_store pdfs temp
```

## 🚀 Kullanım Örnekleri

### 1. Belge Yükleme ve İndeksleme
```python
from rag import DocumentProcessor, VectorStore, SearchService

# Bileşenleri başlat
doc_processor = DocumentProcessor()
vector_store = VectorStore()
search_service = SearchService(vector_store, doc_processor)

# PDF dosyası yükle
result = search_service.add_document_to_index("path/to/document.pdf")
print(f"Oluşturulan chunk sayısı: {result['chunks_created']}")
```

### 2. Arama Yapma
```python
# Genel arama
results = search_service.search_documents(
    query="Python programlama",
    k=5,
    filter_by_type="pdf"
)

# Roadmap araması
roadmap_results = search_service.search_roadmaps(
    query="web geliştirme",
    k=3
)
```

### 3. Tavsiye Alma
```python
from rag import RecommendationService

recommendation_service = RecommendationService(search_service)

# Öğrenme tavsiyeleri
recommendations = recommendation_service.get_learning_recommendations(
    user_interests=["Python", "Web Development"],
    user_level="beginner",
    max_recommendations=5
)
```

### 4. PDF Oluşturma
```python
from rag import PDFGenerator

pdf_generator = PDFGenerator()

# Roadmap PDF'i oluştur
pdf_path = pdf_generator.generate_roadmap_pdf(
    roadmap_data=roadmap_data,
    user_info={"name": "John Doe", "email": "john@example.com"}
)
```

## 📡 API Endpoint'leri

### Belge Yönetimi
- `POST /rag/upload-document` - Belge yükleme
- `POST /rag/add-roadmap` - Roadmap ekleme
- `POST /rag/add-blog-content` - Blog içeriği ekleme

### Arama
- `GET /rag/search` - Genel arama
- `GET /rag/search-roadmaps` - Roadmap araması
- `GET /rag/search-educational` - Eğitim içeriği araması
- `GET /rag/get-context` - İlgili bağlam alma

### Tavsiyeler
- `POST /rag/recommendations/learning` - Öğrenme tavsiyeleri
- `POST /rag/recommendations/next-steps` - Sonraki adım tavsiyeleri
- `POST /rag/recommendations/personalized` - Kişiselleştirilmiş içerik
- `GET /rag/recommendations/daily` - Günlük tavsiyeler
- `GET /rag/recommendations/related` - İlgili içerik

### PDF Oluşturma
- `POST /rag/generate-pdf/roadmap` - Roadmap PDF'i
- `POST /rag/generate-pdf/progress` - İlerleme raporu PDF'i
- `POST /rag/generate-pdf/summary` - Öğrenme özeti PDF'i

### Yönetim
- `GET /rag/stats` - Sistem istatistikleri
- `DELETE /rag/clear-index` - Index temizleme
- `POST /rag/cleanup-pdfs` - PDF temizleme

## 🔍 Chunking Stratejisi Detayları

### Chunk Boyutları
- **Varsayılan**: 1000 karakter
- **Overlap**: 200 karakter
- **Ayarlanabilir**: İhtiyaca göre değiştirilebilir

### Bölme Stratejisi
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
```

### Metadata Yapısı
```python
metadata = {
    "source": "file_path",
    "chunk_id": 0,
    "file_type": "pdf|text|blog|roadmap",
    "total_chunks": 10,
    "roadmap_id": "optional",
    "roadmap_title": "optional"
}
```

## 🗄️ VectorDB Seçenekleri

### Chroma DB (Önerilen)
**Avantajlar:**
- Yerel kurulum, internet bağımlılığı yok
- Metadata filtreleme desteği
- Kolay yönetim ve bakım
- Hızlı sorgu performansı

**Kullanım:**
```python
vector_store = VectorStore(
    store_type="chroma",
    embedding_model="huggingface",
    persist_directory="./vector_store"
)
```

### FAISS
**Avantajlar:**
- Çok hızlı benzerlik arama
- Büyük veri setleri için optimize
- GPU desteği (opsiyonel)

**Kullanım:**
```python
vector_store = VectorStore(
    store_type="faiss",
    embedding_model="openai",
    persist_directory="./vector_store"
)
```

## 🧠 Embedding Modelleri (Ücretsiz)

### HuggingFace Embeddings (Varsayılan)
- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Boyut**: 384 boyut
- **Kalite**: İyi
- **Maliyet**: Ücretsiz, yerel çalışır
- **Hız**: Hızlı
- **Kullanım**: Genel amaçlı arama

### Sentence Transformers (Çok Dilli)
- **Model**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Boyut**: 384 boyut
- **Kalite**: İyi
- **Maliyet**: Ücretsiz, yerel çalışır
- **Hız**: Orta
- **Kullanım**: Çok dilli içerik için

### Instructor Embeddings (Yüksek Kalite)
- **Model**: hkunlp/instructor-large
- **Boyut**: 768 boyut
- **Kalite**: Yüksek
- **Maliyet**: Ücretsiz, yerel çalışır
- **Hız**: Yavaş
- **Kullanım**: Hassas arama için

## 📊 Performans Optimizasyonu

### 1. Chunk Boyutu Optimizasyonu
- **Küçük chunk'lar**: Daha spesifik sonuçlar, daha fazla chunk
- **Büyük chunk'lar**: Daha geniş bağlam, daha az chunk
- **Önerilen**: 800-1200 karakter arası

### 2. Embedding Model Seçimi
- **Hızlı arama**: HuggingFace embeddings (all-MiniLM-L6-v2)
- **Çok dilli içerik**: Sentence Transformers (multilingual-MiniLM-L12-v2)
- **Yüksek kalite**: Instructor embeddings (instructor-large)
- **Varsayılan**: HuggingFace embeddings (en iyi denge)

### 3. VectorDB Optimizasyonu
- **Küçük veri setleri**: Chroma DB
- **Büyük veri setleri**: FAISS
- **Metadata filtreleme**: Chroma DB

## 🔒 Güvenlik ve Gizlilik

### 1. Veri Güvenliği
- Tüm dosyalar yerel olarak saklanır
- API anahtarları environment variables'da
- Kullanıcı verileri şifrelenir

### 2. Erişim Kontrolü
- Tüm endpoint'ler authentication gerektirir
- Kullanıcı bazlı veri izolasyonu
- Rate limiting uygulanabilir

### 3. Veri Temizliği
- Geçici dosyalar otomatik silinir
- Eski PDF'ler zamanla temizlenir
- Index'ler düzenli olarak optimize edilir

## 🐛 Hata Ayıklama

### Yaygın Hatalar ve Çözümleri

1. **Chroma DB Bağlantı Hatası**
   ```bash
   # Dizin izinlerini kontrol et
   chmod 755 ./vector_store
   ```

2. **PDF İşleme Hatası**
   ```bash
   # PyMuPDF kurulumunu kontrol et
   pip install --upgrade PyMuPDF
   ```

3. **Embedding Model Hatası**
   ```bash
   # Sentence transformers'ı yeniden kur
   pip install --upgrade sentence-transformers
   ```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🚀 Gelecek Geliştirmeler

### Planlanan Özellikler
1. **Çoklu Dil Desteği**: Farklı dillerde arama ve tavsiye
2. **Görsel İçerik**: Resim ve video analizi
3. **Gerçek Zamanlı Güncelleme**: Canlı içerik indeksleme
4. **Gelişmiş Filtreleme**: Daha detaylı arama filtreleri
5. **Performans İzleme**: Detaylı metrikler ve analitikler

### Entegrasyon Fırsatları
1. **External API'ler**: Wikipedia, Stack Overflow entegrasyonu
2. **Social Learning**: Kullanıcı etkileşimleri ve yorumlar
3. **Adaptive Learning**: Kullanıcı davranışlarına göre öğrenme
4. **Gamification**: Başarı rozetleri ve seviye sistemi

## 📞 Destek ve İletişim

Bu RAG sistemi hakkında sorularınız için:
- GitHub Issues kullanın
- Dokümantasyonu kontrol edin
- Test dosyalarını inceleyin

---

**Not**: Bu sistem sürekli geliştirilmektedir. Yeni özellikler ve iyileştirmeler düzenli olarak eklenmektedir.
