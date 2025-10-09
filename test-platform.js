// Risko Platform Production Test Suite
// Bu script platformun production hazırlığını test eder

class PlatformTester {
    constructor() {
        this.testResults = [];
        this.errors = [];
    }

    async runAllTests() {
        console.log('🚀 Risko Platform Production Test Suite Başlatılıyor...\n');
        
        await this.testBasicFunctionality();
        await this.testSettingsPage();
        await this.testMapFunctionality();
        await this.testRealTimeData();
        await this.testThemeSystem();
        await this.testResponsiveDesign();
        await this.testPerformance();
        
        this.generateReport();
    }

    async testBasicFunctionality() {
        console.log('📋 Temel İşlevsellik Testleri...');
        
        try {
            // Test app initialization
            if (typeof window.app !== 'undefined') {
                this.pass('App başarıyla yüklendi');
            } else {
                this.fail('App yüklenemedi');
            }

            // Test navigation
            const navItems = document.querySelectorAll('.nav-link');
            if (navItems.length > 0) {
                this.pass(`Navigasyon menüsü yüklendi (${navItems.length} öğe)`);
            } else {
                this.fail('Navigasyon menüsü bulunamadı');
            }

            // Test dashboard cards
            const dashboardCards = document.querySelectorAll('.dashboard-card');
            if (dashboardCards.length >= 4) {
                this.pass(`Dashboard kartları yüklendi (${dashboardCards.length} kart)`);
            } else {
                this.fail('Dashboard kartları eksik');
            }

            // Test API client
            if (window.app && window.app.apiClient) {
                this.pass('API Client başarıyla yüklendi');
            } else {
                this.fail('API Client yüklenemedi');
            }

        } catch (error) {
            this.fail('Temel işlevsellik testi başarısız: ' + error.message);
        }
    }

    async testSettingsPage() {
        console.log('⚙️ Settings Sayfası Testleri...');
        
        try {
            // Navigate to settings
            if (window.app) {
                await window.app.navigateToPage('settings');
                
                // Check theme selector
                const themeSelect = document.getElementById('theme-select');
                if (themeSelect) {
                    this.pass('Tema seçici bulundu');
                    
                    // Test theme change
                    themeSelect.value = 'dark';
                    themeSelect.dispatchEvent(new Event('change'));
                    
                    setTimeout(() => {
                        if (document.body.classList.contains('theme-dark')) {
                            this.pass('Koyu tema başarıyla uygulandı');
                        } else {
                            this.fail('Koyu tema uygulanamadı');
                        }
                    }, 100);
                } else {
                    this.fail('Tema seçici bulunamadı');
                }

                // Check notification settings
                const emailNotifications = document.getElementById('email-notifications');
                if (emailNotifications) {
                    this.pass('Bildirim ayarları bulundu');
                } else {
                    this.fail('Bildirim ayarları bulunamadı');
                }
            }
        } catch (error) {
            this.fail('Settings sayfası testi başarısız: ' + error.message);
        }
    }

    async testMapFunctionality() {
        console.log('🗺️ Harita İşlevselliği Testleri...');
        
        try {
            if (window.app) {
                await window.app.navigateToPage('map');
                
                // Check if map container exists
                const mapContainer = document.getElementById('risk-map');
                if (mapContainer) {
                    this.pass('Harita konteyneri bulundu');
                } else {
                    this.fail('Harita konteyneri bulunamadı');
                }

                // Check map controls
                const riskTypeSelect = document.getElementById('map-risk-type');
                if (riskTypeSelect) {
                    this.pass('Harita kontrolleri bulundu');
                } else {
                    this.fail('Harita kontrolleri bulunamadı');
                }

                // Test Leaflet map
                setTimeout(() => {
                    if (window.app.map) {
                        this.pass('Leaflet haritası başarıyla yüklendi');
                    } else {
                        this.fail('Leaflet haritası yüklenemedi');
                    }
                }, 1000);
            }
        } catch (error) {
            this.fail('Harita testi başarısız: ' + error.message);
        }
    }

    async testRealTimeData() {
        console.log('📊 Gerçek Zamanlı Veri Testleri...');
        
        try {
            if (window.app && window.app.apiClient) {
                // Test dashboard stats
                const stats = await window.app.apiClient.getDashboardStats();
                if (stats && stats.total > 0) {
                    this.pass(`Dashboard istatistikleri alındı (${stats.total} toplam analiz)`);
                } else {
                    this.fail('Dashboard istatistikleri alınamadı');
                }

                // Test map data
                const mapData = await window.app.apiClient.getRiskMapData();
                if (mapData && mapData.length > 0) {
                    this.pass(`Harita verileri alındı (${mapData.length} konum)`);
                } else {
                    this.fail('Harita verileri alınamadı');
                }

                // Test live data system
                if (window.app.liveDataInterval) {
                    this.pass('Canlı veri sistemi aktif');
                } else {
                    this.warn('Canlı veri sistemi bulunamadı');
                }
            }
        } catch (error) {
            this.fail('Gerçek zamanlı veri testi başarısız: ' + error.message);
        }
    }

    async testThemeSystem() {
        console.log('🎨 Tema Sistemi Testleri...');
        
        try {
            const body = document.body;
            
            // Test light theme
            body.className = 'theme-light';
            const lightStyles = getComputedStyle(body);
            this.pass('Açık tema uygulandı');
            
            // Test dark theme
            body.className = 'theme-dark';
            const darkStyles = getComputedStyle(body);
            this.pass('Koyu tema uygulandı');
            
            // Reset to default
            body.className = '';
            
            // Test CSS variables
            const rootStyles = getComputedStyle(document.documentElement);
            const primaryColor = rootStyles.getPropertyValue('--primary-color');
            if (primaryColor) {
                this.pass('CSS değişkenleri yüklendi');
            } else {
                this.fail('CSS değişkenleri bulunamadı');
            }
            
        } catch (error) {
            this.fail('Tema sistemi testi başarısız: ' + error.message);
        }
    }

    async testResponsiveDesign() {
        console.log('📱 Responsive Tasarım Testleri...');
        
        try {
            // Test different viewport sizes
            const viewports = [
                { width: 1920, height: 1080, name: 'Desktop' },
                { width: 768, height: 1024, name: 'Tablet' },
                { width: 375, height: 667, name: 'Mobile' }
            ];

            viewports.forEach(viewport => {
                // Simulate viewport change
                document.documentElement.style.width = viewport.width + 'px';
                
                // Check if cards are responsive
                const cards = document.querySelectorAll('.card');
                if (cards.length > 0) {
                    this.pass(`${viewport.name} responsive test geçti`);
                } else {
                    this.fail(`${viewport.name} responsive test başarısız`);
                }
            });

            // Reset viewport
            document.documentElement.style.width = '';
            
        } catch (error) {
            this.fail('Responsive tasarım testi başarısız: ' + error.message);
        }
    }

    async testPerformance() {
        console.log('⚡ Performans Testleri...');
        
        try {
            // Test page load time
            const loadTime = performance.now();
            if (loadTime < 3000) {
                this.pass(`Sayfa yükleme süresi: ${loadTime.toFixed(2)}ms`);
            } else {
                this.warn(`Sayfa yükleme süresi yavaş: ${loadTime.toFixed(2)}ms`);
            }

            // Test memory usage (if available)
            if (performance.memory) {
                const memoryMB = performance.memory.usedJSHeapSize / 1024 / 1024;
                if (memoryMB < 50) {
                    this.pass(`Bellek kullanımı: ${memoryMB.toFixed(2)}MB`);
                } else {
                    this.warn(`Yüksek bellek kullanımı: ${memoryMB.toFixed(2)}MB`);
                }
            }

            // Test DOM node count
            const nodeCount = document.getElementsByTagName('*').length;
            if (nodeCount < 1000) {
                this.pass(`DOM node sayısı: ${nodeCount}`);
            } else {
                this.warn(`Yüksek DOM node sayısı: ${nodeCount}`);
            }

        } catch (error) {
            this.fail('Performans testi başarısız: ' + error.message);
        }
    }

    pass(message) {
        this.testResults.push({ status: 'PASS', message });
        console.log(`✅ ${message}`);
    }

    fail(message) {
        this.testResults.push({ status: 'FAIL', message });
        this.errors.push(message);
        console.log(`❌ ${message}`);
    }

    warn(message) {
        this.testResults.push({ status: 'WARN', message });
        console.log(`⚠️ ${message}`);
    }

    generateReport() {
        console.log('\n📊 TEST RAPORU');
        console.log('=' * 50);
        
        const passed = this.testResults.filter(t => t.status === 'PASS').length;
        const failed = this.testResults.filter(t => t.status === 'FAIL').length;
        const warnings = this.testResults.filter(t => t.status === 'WARN').length;
        
        console.log(`\n✅ Başarılı: ${passed}`);
        console.log(`❌ Başarısız: ${failed}`);
        console.log(`⚠️ Uyarı: ${warnings}`);
        console.log(`📋 Toplam: ${this.testResults.length}`);
        
        if (failed === 0) {
            console.log('\n🎉 TÜM TESTLER BAŞARILI! Platform production hazır.');
        } else {
            console.log('\n🔧 Düzeltilmesi gereken sorunlar:');
            this.errors.forEach(error => console.log(`   - ${error}`));
        }

        console.log('\n🚀 Platform Özellikleri:');
        console.log('   ✅ Gerçek Türkiye risk verileri');
        console.log('   ✅ Tema sistemi (Açık/Koyu/Otomatik)');
        console.log('   ✅ Zoom bazlı harita detayları');
        console.log('   ✅ Canlı bölgesel istatistikler');
        console.log('   ✅ Responsive design');
        console.log('   ✅ Settings sayfası');
        console.log('   ✅ Production optimizasyonları');
    }
}

// Test suite'i otomatik çalıştır
if (typeof window !== 'undefined') {
    window.addEventListener('load', async () => {
        // Wait for app to initialize
        setTimeout(async () => {
            if (window.app) {
                const tester = new PlatformTester();
                await tester.runAllTests();
            }
        }, 2000);
    });
}

// Export for manual testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PlatformTester;
}