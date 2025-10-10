// Risko Configuration (unified for all environments)
(function(){
    const storedApi = (typeof localStorage !== 'undefined') ? localStorage.getItem('risko_api_base') : null;
    const defaultApi = storedApi || 'http://localhost:8000';
    window.RISKO_CONFIG = {
        // API Configuration
        API_BASE_URL: defaultApi,

        // Demo Mode (always off for real functionality)
        DEMO_MODE: false,
        DEMO_BANNER: false,

        // Analytics
        GOOGLE_ANALYTICS_ID: '',

        // Feature Flags
        FEATURES: {
            ANALYTICS: true,
            FORM_VALIDATION: true,
            ANIMATIONS: true,
            DEBUG_MODE: false,
            DETAILED_ANALYSIS: true,
            BATCH_ANALYSIS: true,
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
            SHOW_DEMO_DATA: false,
            ANIMATION_SPEED: 'normal',
            THEME: 'black',
            DARK_MODE: 'dark',
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

    // Auto-detect environment (DEMO_MODE stays false)
    const hostname = window.location.hostname;
    if (hostname.includes('github.io')) {
        window.RISKO_CONFIG.ENVIRONMENT = 'github-pages';
        console.log('🚀 Risko Platform GitHub Pages üzerinde (gerçek API)');
    } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
        window.RISKO_CONFIG.FEATURES.DEBUG_MODE = true;
        window.RISKO_CONFIG.ENVIRONMENT = 'development';
        window.RISKO_CONFIG.API_BASE_URL = defaultApi;
        console.log('🛠️ Risko Platform geliştirme modunda (gerçek API)');
    } else {
        window.RISKO_CONFIG.ENVIRONMENT = 'production';
        console.log('🌟 Risko Platform production modunda');
    }
})();