// Risko Platform Configuration
window.RISKO_CONFIG = {
    // API Configuration
    API_BASE_URL: 'http://localhost:8001', // Backend API URL
    
    // Demo Mode - set to true for GitHub Pages deployment
    DEMO_MODE: true, // Using demo mode for GitHub Pages
    DEMO_BANNER: false,
    
    // Analytics
    GOOGLE_ANALYTICS_ID: '', // Add your GA4 ID here
    
    // Feature Flags
    FEATURES: {
        ANALYTICS: true,
        FORM_VALIDATION: true,
        ANIMATIONS: true,
        DEBUG_MODE: false, // Set to true for development
        DETAILED_ANALYSIS: true,
        BATCH_ANALYSIS: true, // Premium feature
        PREMIUM_FEATURES: true,
        RECOMMENDATIONS: true,
        NOTIFICATIONS: true,
        REAL_TIME_UPDATES: true,
        MAP_INTEGRATION: true,
        PDF_EXPORT: true,
        API_ACCESS: true
    },
    
    // UI Settings
    UI: {
        SHOW_DEMO_DATA: true,
        ANIMATION_SPEED: 'normal',
        THEME: 'default',
        DARK_MODE: 'auto', // auto, light, dark
        SIDEBAR_COLLAPSED: false
    },
    
    // Theme Configuration
    THEME: {
        PRIMARY_COLOR: '#4f46e5',
        SECONDARY_COLOR: '#10b981',
        ACCENT_COLOR: '#f59e0b'
    },
    
    // API Endpoints
    ENDPOINTS: {
        RISK_ANALYZE: '/risk/analyze',
        BATCH_ANALYZE: '/risk/batch-analyze',
        MAP_DATA: '/risk/map-data',
        REPORTS: '/reports',
        USER_PROFILE: '/user/profile',
        ACTIVITIES: '/activities'
    },
    
    // Premium Plans
    PLANS: {
        FREE: { analyses_per_month: 5, api_access: false },
        PRO: { analyses_per_month: 100, api_access: true, price: 99 },
        ENTERPRISE: { analyses_per_month: -1, api_access: true, price: 499 }
    },
    
    // Deployment Information
    VERSION: '2.0.0',
    BUILD_DATE: new Date().toISOString(),
    ENVIRONMENT: 'production'
};

// Auto-detect environment and adjust settings
(function() {
    const hostname = window.location.hostname;
    
    if (hostname.includes('github.io')) {
        // GitHub Pages deployment
        window.RISKO_CONFIG.DEMO_MODE = true;
        window.RISKO_CONFIG.ENVIRONMENT = 'github-pages';
        console.log('🚀 Kürşat\'ın Risko Platform\'u GitHub Pages\'te çalışıyor');
    } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
        // Local development
        window.RISKO_CONFIG.FEATURES.DEBUG_MODE = true;
        window.RISKO_CONFIG.ENVIRONMENT = 'development';
        console.log('🛠️ Kürşat\'ın Risko Platform\'u geliştirme modunda');
    } else {
        // Production deployment
        window.RISKO_CONFIG.DEMO_MODE = false; // Set to true if API is not ready
        window.RISKO_CONFIG.ENVIRONMENT = 'production';
        console.log('🌟 Kürşat\'ın Risko Platform\'u production modunda');
    }
})();