// Enhanced error-safe initialization with better loading
window.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Risko başlatılıyor...');
    
    // Initialize theme immediately
    const savedTheme = localStorage.getItem('risko-theme');
    const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const theme = savedTheme || systemPreference;
    document.documentElement.setAttribute('data-theme', theme);
    
    // Enhanced library loading check
    let attempts = 0;
    const maxAttempts = 20; // 10 seconds max wait
    
    function initializeWhenReady() {
        attempts++;
        
        // Check if all required libraries are loaded
        const chartLoaded = typeof Chart !== 'undefined';
        const leafletLoaded = typeof L !== 'undefined';
        const swalLoaded = typeof Swal !== 'undefined';
        const bootstrapLoaded = typeof bootstrap !== 'undefined';
        
        if (!chartLoaded || !leafletLoaded || !swalLoaded) {
            if (attempts >= maxAttempts) {
                console.warn('⚠️ Some libraries failed to load, starting with fallback mode...');
                initializeFallbackMode();
                return;
            }
            
            console.log(`⏳ Kütüphaneler yükleniyor... (${attempts}/${maxAttempts})`);
            setTimeout(initializeWhenReady, 500);
            return;
        }
        
        console.log('✅ Tüm kütüphaneler yüklendi, platform başlatılıyor...');
        
        try {
            window.app = new RiskoPlatformApp();
            console.log('🚀 Risko başarıyla başlatıldı!');
        } catch (error) {
            console.error('❌ Platform başlatma hatası:', error);
            console.error('Stack trace:', error.stack);
            
            // Show detailed error for debugging
            if (error.message.includes('setupDataRefresh')) {
                console.error('🔧 setupDataRefresh metodunun tanımlanması gerekiyor');
            }
            
            initializeFallbackMode();
        }
    }
    
    function initializeFallbackMode() {
        // Hide loading screen
        document.getElementById('loading-screen').classList.add('d-none');
        document.getElementById('app').classList.remove('d-none');
        
        // Show notification
        const notification = document.createElement('div');
        notification.className = 'alert alert-warning position-fixed top-0 start-50 translate-middle-x mt-3';
        notification.style.zIndex = '9999';
        notification.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Basit Mod:</strong> Platform basit modda çalışıyor. Tüm özellikler için sayfayı yenileyin.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);
        
        // Initialize basic functionality
        initializeBasicFunctionality();
    }
    
    function initializeBasicFunctionality() {
        // Basic theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('risko-theme', newTheme);
                console.log(`🎨 Tema değiştirildi: ${newTheme}`);
            });
        }
        
        // Basic navigation
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-page]')) {
                e.preventDefault();
                const page = e.target.closest('[data-page]').getAttribute('data-page');
                console.log(`📄 Sayfa geçişi: ${page}`);
                
                // Hide all pages
                document.querySelectorAll('.page-content').forEach(p => {
                    p.classList.remove('active');
                });
                
                // Show target page or dashboard
                const targetPage = document.getElementById(`${page}-page`) || document.getElementById('dashboard-page');
                if (targetPage) {
                    targetPage.classList.add('active');
                }
            }
        });
        
        // Update user info
        const userName = document.getElementById('user-name');
        if (userName) {
            userName.textContent = 'Kürşat';
        }
        
        const userAvatar = document.getElementById('user-avatar');
        if (userAvatar) {
            userAvatar.src = 'https://ui-avatars.com/api/?name=Kursat&background=4f46e5&color=fff&size=32';
        }
    }
    
    // Start initialization
    initializeWhenReady();
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', () => {
        if (window.app && document.visibilityState === 'visible') {
            console.log('👀 Sayfa görünür, veriler yenileniyor...');
            if (window.app.currentPage === 'dashboard') {
                window.app.refreshDashboardData();
            }
        }
    });
    
    // Add performance monitoring
    window.addEventListener('load', () => {
        console.log('⚡ Sayfa tamamen yüklendi');
        
        // Log performance metrics
        if (window.performance && window.performance.timing) {
            const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
            console.log(`📊 Yükleme süresi: ${loadTime}ms`);
        }
    });
});