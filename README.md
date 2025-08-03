# MyWisePath - Kişiselleştirilmiş Öğrenme Platformu

MyWisePath, kullanıcıların kişisel öğrenme yolculuklarını planlamalarına ve takip etmelerine yardımcı olan bir platformdur. AI destekli öneriler, interaktif chatbot ve kişiselleştirilmiş roadmap'ler sunar.

## 🚀 Özellikler

- **AI Destekli Öğrenme Önerileri**: Gemini AI ile kişiselleştirilmiş içerik önerileri
- **İnteraktif Chatbot**: Öğrenme sürecinde yardım ve rehberlik
- **Kişiselleştirilmiş Roadmap**: Hedeflerinize uygun öğrenme yolları
- **E-posta Otomasyonu**: Haftalık hatırlatıcılar ve ilerleme raporları
- **Modern Web Arayüzü**: React ile geliştirilmiş kullanıcı dostu arayüz

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
```

3. **Backend'i başlatın:**
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

E-posta otomasyonunu test etmek için:

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
│   │   └── automation.py         # E-posta otomasyonu
│   ├── services/                  # İş mantığı servisleri
│   │   ├── ai_service.py         # AI servisleri
│   │   ├── educational_content_service.py  # İçerik servisleri
│   │   ├── email_service.py      # E-posta servisi
│   │   └── automation_service.py # Otomasyon servisi
│   └── models/                    # Veri modelleri
├── frontend/                      # React uygulaması
└── test_email_automation.py      # E-posta otomasyonu test dosyası
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
