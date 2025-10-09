# Risko Platform - GitHub Pages Deployment

Evet, **GitHub Pages ile dağıtım mükemmel bir seçenek!** Local'de çalışmadığı için bu yol çok mantıklı. İşte hazırladığım tam rehber:

## 🚀 GitHub Pages Deployment Rehberi

### 1. Repository Ayarları

1. **GitHub repository'nize gidin**
2. **Settings > Pages** sekmesine tıklayın
3. **Source** olarak "**GitHub Actions**" seçin
4. Save butonuna tıklayın

### 2. Dosyaları Push Edin

```bash
git add .
git commit -m "🚀 GitHub Pages deployment setup"
git push origin main
```

### 3. Deployment Süreci

- Push yaptığınızda otomatik olarak GitHub Actions çalışacak
- **Actions** sekmesinden deployment durumunu izleyebilirsiniz
- Yaklaşık 2-3 dakika içinde siteniz hazır olacak

### 4. Site URL'niz

Site şu adreste yayınlanacak:
```
https://[username].github.io/risko/
```

## ✨ Hazırladığım Özellikler

### Frontend Özellikleri
- ✅ **Responsive tasarım** (mobil uyumlu)
- ✅ **Modern UI/UX** (Bootstrap 5 + özel CSS)
- ✅ **Demo modu** (API olmadan çalışır)
- ✅ **Risk analizi formu** (interaktif)
- ✅ **Animasyonlar** ve geçişler
- ✅ **Font Awesome** ikonları

### Teknik Özellikler
- ✅ **GitHub Actions** otomatik deployment
- ✅ **Statik hosting** optimizasyonu
- ✅ **Configurable API** endpoints
- ✅ **Demo data** sistemi
- ✅ **Error handling** ve fallbacks

## 🔧 Yapılandırma

### config.js Dosyası
- **Demo modu:** GitHub Pages'de otomatik aktif
- **API URL:** Backend hazır olduğunda değiştirilebilir
- **Feature flags:** Özellikler açılıp kapatılabilir

### Gelecek İçin Planlama
1. **Backend API:** Railway/Render/Heroku'ya deploy
2. **Custom domain:** Opsiyonel profesyonel domain
3. **Analytics:** Google Analytics entegrasyonu

## 🎯 İlk Adımlar

1. Repository **Settings > Pages** ayarını yapın
2. Bu değişiklikleri **push** edin
3. **Actions** sekmesinden deployment'ı izleyin
4. Site hazır olduğunda test edin

## 📱 Demo Özellikleri

Site demo modunda şu özellikleri sunuyor:
- Risk analizi formu
- Örnek risk hesaplamaları
- Şirket bilgileri
- İletişim formu
- Responsive tasarım

Herşey hazır! 🎉 Push ettikten sonra siteniz otomatik olarak yayınlanacak.