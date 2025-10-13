// Risko Configuration (unified for all environments)
//
// This file centralizes frontend configuration for development and production.
// - For local development (docker-compose) the frontend will automatically
//   use the backend at http://localhost:8000 so the app works "out of the box".
// - In production you should override `window.RISKO_CONFIG.API_BASE_URL` via
//   your deployment environment or set a different value here before build.
// - This file will NOT prompt the user for any values. Interactive prompts
//   caused confusion and have been removed to ensure consistent developer UX.
(function(){
    const getParam = (key) => { try { return new URLSearchParams(window.location.search).get(key); } catch { return null; } };
    // Respect an explicitly set localStorage value or query param when present,
    // but do NOT prompt the user. Default to the local development backend.
    let storedApi = (typeof localStorage !== 'undefined') ? localStorage.getItem('risko_api_base') : null;
    const qp = getParam('api') || getParam('api_base');
    if (!storedApi && qp && /^https?:\/\//i.test(qp)) {
        try { localStorage.setItem('risko_api_base', qp); storedApi = qp; } catch {}
    }
    // Default development API base (matches docker-compose dev backend)
    // IMPORTANT: when served from GitHub Pages we must NOT default to localhost
    // because that causes pages to attempt connections to the developer's
    // machine (ERR_CONNECTION_REFUSED). Instead default to empty and require
    // an explicit API_BASE_URL when on GitHub Pages.
    const hostname = (typeof window !== 'undefined' && window.location && window.location.hostname) ? window.location.hostname : '';
    const defaultApi = storedApi || (hostname.includes('github.io') ? '' : 'http://localhost:8000');
    window.RISKO_CONFIG = {
        // API Configuration
        API_BASE_URL: defaultApi,
        // Indicate auth provider so frontend picks up Supabase config
        auth_provider: 'supabase',
    // Supabase configuration (in production this should be injected at deploy time)
    // NOTE: Do NOT commit secrets (service-role keys) to the repository. The
    // public anon key is safe for client usage but we still prefer injecting
    // both values via CI runtime config (see .github/workflows/deploy_github_pages.yml).
    supabase_url: '',
    supabase_anon_key: '',

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
            RISK_ANALYZE: '/analyze',
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

    // Auto-detect environment (DEMO_MODE stays false). No interactive prompts.
    // Auto-detect environment and avoid defaulting to localhost on github.io
    if (hostname.includes('github.io')) {
        window.RISKO_CONFIG.ENVIRONMENT = 'github-pages';
        // Do not set API_BASE_URL to localhost on GitHub Pages; prefer explicit config
        if (storedApi) {
            window.RISKO_CONFIG.API_BASE_URL = storedApi;
        } else {
            window.RISKO_CONFIG.API_BASE_URL = '';
        }
        console.log('🚀 Risko Platform GitHub Pages (no prompt)');
    } else if (hostname === 'localhost' || hostname === '127.0.0.1') {
        window.RISKO_CONFIG.FEATURES.DEBUG_MODE = true;
        window.RISKO_CONFIG.ENVIRONMENT = 'development';
        // For local development we default to the docker-compose backend port
        window.RISKO_CONFIG.API_BASE_URL = defaultApi;
        console.log('🛠️ Risko Platform development (API -> ' + window.RISKO_CONFIG.API_BASE_URL + ')');
    } else {
        window.RISKO_CONFIG.ENVIRONMENT = 'production';
        // For production rely on the configured API_BASE_URL (default may be localhost)
        if (storedApi) window.RISKO_CONFIG.API_BASE_URL = storedApi;
        console.log('🌟 Risko Platform production (no prompt)');
    }
})();