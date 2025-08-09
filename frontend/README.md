# MyWisePath Frontend

Modern, kullanıcı dostu ve kişiselleştirilmiş öğrenme platformu için yeniden tasarlanmış frontend uygulaması.

## 🎨 Tasarım Sistemi

### Renk Paleti
- **Primary**: Modern indigo (#6366f1) - Ana aksiyonlar ve vurgular için
- **Secondary**: Amber (#f59e0b) - İkincil aksiyonlar ve uyarılar için
- **Success**: Emerald (#10b981) - Başarı durumları için
- **Warning**: Amber (#f59e0b) - Uyarılar için
- **Error**: Red (#ef4444) - Hata durumları için
- **Info**: Blue (#3b82f6) - Bilgi mesajları için

### Tipografi
- **Font Family**: Inter, Roboto, Helvetica, Arial
- **Başlıklar**: Bold (700) ve Medium (600) ağırlıklar
- **Gövde Metni**: Normal (400) ağırlık, 1.6 line-height

### Bileşen Stilleri
- **Border Radius**: 8px (küçük), 12px (orta), 16px (büyük)
- **Gölgeler**: Subtle shadows with hover effects
- **Animasyonlar**: Smooth transitions (0.2s-0.3s ease-in-out)

## 🚀 Özellikler

### Modern UI/UX
- ✅ **Glassmorphism** efektleri
- ✅ **Gradient** arka planlar
- ✅ **Smooth animations** ve geçişler
- ✅ **Responsive design** (mobile-first)
- ✅ **Accessibility** standartları
- ✅ **Dark mode** hazırlığı

### Kullanıcı Deneyimi
- ✅ **Intuitive navigation** - Kolay gezinme
- ✅ **Progressive disclosure** - Aşamalı bilgi gösterimi
- ✅ **Loading states** - Yükleme durumları
- ✅ **Error handling** - Hata yönetimi
- ✅ **Feedback mechanisms** - Geri bildirim mekanizmaları

### Teknik Özellikler
- ✅ **TypeScript** - Tip güvenliği
- ✅ **Material-UI v5** - Modern component library
- ✅ **React Router v6** - Client-side routing
- ✅ **Context API** - State management
- ✅ **Error Boundaries** - Hata yakalama
- ✅ **Lazy Loading** - Performans optimizasyonu

## 📁 Proje Yapısı

```
src/
├── components/          # Yeniden kullanılabilir bileşenler
│   ├── Navigation.tsx  # Modern navigasyon
│   ├── LoadingSpinner.tsx # Yükleme animasyonu
│   ├── ErrorBoundary.tsx # Hata yakalama
│   └── ...
├── pages/              # Sayfa bileşenleri
│   ├── Login.tsx       # Modern giriş sayfası
│   ├── Register.tsx    # Modern kayıt sayfası
│   ├── Dashboard.tsx   # Yeniden tasarlanmış dashboard
│   ├── Roadmap.tsx     # İyileştirilmiş yol haritası
│   └── ...
├── contexts/           # React Context'leri
├── services/           # API servisleri
├── types/              # TypeScript tip tanımları
└── utils/              # Yardımcı fonksiyonlar
```

## 🎯 Tasarım Prensipleri

### 1. Kullanıcı Merkezli Tasarım
- Her etkileşim anlamlı geri bildirim sağlar
- Kullanıcı yolculuğu optimize edilmiştir
- Erişilebilirlik standartlarına uygun

### 2. Görsel Hiyerarşi
- Net başlık yapısı (H1-H6)
- Tutarlı boşluk kullanımı
- Renk ve tipografi ile vurgu

### 3. Tutarlılık
- Tüm bileşenler aynı tasarım dilini kullanır
- Standart spacing ve sizing
- Tutarlı animasyon süreleri

### 4. Performans
- Lazy loading ve code splitting
- Optimized bundle size
- Smooth 60fps animations

## 🛠️ Kurulum

```bash
# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm start

# Production build
npm run build

# Test'leri çalıştır
npm test
```

## 🎨 Tema Özelleştirme

Tema dosyası `src/App.tsx` içinde tanımlanmıştır. Ana özelleştirme noktaları:

```typescript
const theme = createTheme({
  palette: {
    primary: { main: '#6366f1' },
    secondary: { main: '#f59e0b' },
    // ...
  },
  typography: {
    fontFamily: '"Inter", "Roboto", ...',
    // ...
  },
  components: {
    MuiButton: { /* Button stilleri */ },
    MuiCard: { /* Card stilleri */ },
    // ...
  },
});
```

## 📱 Responsive Design

- **Mobile First** yaklaşımı
- **Breakpoints**: xs(0), sm(600), md(900), lg(1200), xl(1536)
- **Flexible Grid** sistemi
- **Touch-friendly** etkileşimler

## ♿ Accessibility

- **WCAG 2.1** standartlarına uygun
- **Keyboard navigation** desteği
- **Screen reader** uyumluluğu
- **High contrast** modu hazırlığı
- **Focus indicators** görünür

## 🚀 Gelecek Geliştirmeler

- [ ] **Dark Mode** implementasyonu
- [ ] **PWA** desteği
- [ ] **Offline** çalışma
- [ ] **Advanced animations** (Framer Motion)
- [ ] **Micro-interactions** ekleme
- [ ] **Voice navigation** desteği

## 📊 Performans Metrikleri

- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

**MyWisePath** - Kişiselleştirilmiş öğrenme deneyimi için modern teknoloji ✨
