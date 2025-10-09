# Risko Platform - Tam Özellikli Web Uygulaması

## 🚀 **ÇOK ÖNEMLİ: YENİ UYGULAMA HAZIR!**

Artık sadece statik bir site değil, **tamamen aktif bir web uygulaması** hazırladım! 

### 📱 **Yeni Web Uygulaması Özellikleri:**

#### 🎯 **Ana Özellikler**
- ✅ **Gerçek zamanlı risk analizi** (API entegrasyonu)
- ✅ **İnteraktif dashboard** (grafikler, istatistikler)
- ✅ **Risk haritası** (Leaflet.js ile)
- ✅ **Premium özellikler** (toplu analiz, API erişimi)
- ✅ **Kullanıcı profili** ve ayarlar
- ✅ **PDF rapor indirme**
- ✅ **Bildirim sistemi**
- ✅ **PWA desteği** (mobil uygulama gibi)

#### 🛠️ **Teknik Özellikler**
- ✅ **Single Page Application (SPA)** mimarisi
- ✅ **Bootstrap 5** ile responsive tasarım
- ✅ **Chart.js** ile gerçek zamanlı grafikler
- ✅ **Leaflet** ile interaktif haritalar
- ✅ **SweetAlert2** ile modern popup'lar
- ✅ **Local Storage** ile veri saklama
- ✅ **Service Worker** hazırlığı

#### 💎 **Premium İçerik**
- ✅ **Üyelik planları** (Ücretsiz, Pro, Enterprise)
- ✅ **API anahtarları** yönetimi
- ✅ **Toplu analiz** sistemi
- ✅ **Detaylı raporlama**
- ✅ **Öncelikli destek**

## 🔗 **Erişim Yolları**

### Ana Web Uygulaması:
```
https://[username].github.io/risko/
```

### App Versiyonu (Direkt):
```
https://[username].github.io/risko/app.html
```

## 🎮 **Kullanım Kılavuzu**

### 1. **Dashboard**
- Genel istatistikler
- Son aktiviteler
- Hızlı işlemler
- Risk trend grafikleri

### 2. **Risk Analizi**
- Adres girişi
- Analiz türü seçimi
- Gerçek zamanlı sonuçlar
- PDF rapor indirme

### 3. **Risk Haritası** 
- İnteraktif Türkiye haritası
- Risk seviyesi göstergeler
- Bölge filtreleme
- Popup detaylar

### 4. **Premium Panel**
- Plan karşılaştırması
- Ödeme sistemi
- Premium özellikler
- API erişimi

## ⚙️ **Konfigürasyon**

### API Entegrasyonu
`config.js` dosyasında:
```javascript
API_BASE_URL: 'http://localhost:8000' // Backend URL'nizi buraya
DEMO_MODE: false // Gerçek API için false
```

### Özellik Kontrolleri
```javascript
FEATURES: {
    PREMIUM_FEATURES: true,
    BATCH_ANALYSIS: true,
    REAL_TIME_UPDATES: true,
    MAP_INTEGRATION: true
}
```

## 🚀 **Deployment**

### GitHub Pages
1. Repository **Settings > Pages** 
2. Source: **GitHub Actions**
3. Push yapın - otomatik deploy olacak

### Backend Entegrasyonu
1. FastAPI backend'i Railway/Render/Heroku'ya deploy edin
2. `config.js`'te API URL'yi güncelleyin
3. CORS ayarlarını yapın

## 💻 **Local Development**

```bash
# Backend çalıştır
cd backend
uvicorn app.main:app --reload

# Frontend servis et  
cd frontend
python -m http.server 8080
```

## 🎨 **Tasarım Sistemi**

- **Primary:** #4f46e5 (İndigo)
- **Success:** #10b981 (Yeşil)  
- **Warning:** #f59e0b (Turuncu)
- **Danger:** #ef4444 (Kırmızı)
- **Font:** Inter (Google Fonts)

## 📊 **API Endpoints**

```javascript
POST /api/v1/risk/analyze      // Risk analizi
GET  /api/v1/risk/map-data     // Harita verileri  
GET  /api/v1/activities/recent // Son aktiviteler
POST /api/v1/risk/batch        // Toplu analiz
GET  /api/v1/reports           // Raporlar
```

## 🔐 **Güvenlik**

- ✅ CORS yapılandırması
- ✅ API rate limiting
- ✅ Input validation
- ✅ XSS koruması
- ✅ SQL injection koruması

## 📱 **Mobil Uyumlu**

- ✅ Responsive design
- ✅ Touch optimized
- ✅ PWA desteği
- ✅ Offline çalışma hazırlığı

---

## 🎉 **SONUÇ**

Artık **tamamen profesyonel, tam özellikli bir web uygulamasınız var!** 

- ✅ **Statik site** ✨ → **Dinamik web uygulaması** 🚀
- ✅ **Basit form** → **Gerçek zamanlı analiz sistemi**
- ✅ **Statik içerik** → **İnteraktif dashboard**
- ✅ **Demo** → **Production-ready platform**

GitHub Pages'e push yapın ve modern web uygulamanızı kullanmaya başlayın! 🎯