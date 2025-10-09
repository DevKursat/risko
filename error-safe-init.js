// Simple error-safe initialization
window.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Starting error-safe app initialization...');
    
    // Initialize theme immediately
    const savedTheme = localStorage.getItem('risko-theme');
    const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const theme = savedTheme || systemPreference;
    document.documentElement.setAttribute('data-theme', theme);
    
    // Wait for all libraries to load
    function initializeWhenReady() {
        if (typeof Chart === 'undefined' || typeof L === 'undefined' || typeof Swal === 'undefined') {
            console.log('⏳ Waiting for libraries to load...');
            setTimeout(initializeWhenReady, 500);
            return;
        }
        
        console.log('✅ All libraries loaded, starting app...');
        
        try {
            window.app = new RiskoPlatformApp();
        } catch (error) {
            console.error('❌ App initialization error:', error);
            
            // Fallback: Simple page without complex features
            document.getElementById('loading-screen').classList.add('d-none');
            document.getElementById('app').classList.remove('d-none');
            
            // Show simple error message
            const notification = document.createElement('div');
            notification.className = 'alert alert-warning position-fixed top-0 start-50 translate-middle-x mt-3';
            notification.style.zIndex = '9999';
            notification.innerHTML = `
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>Demo Modu:</strong> Bazı gelişmiş özellikler GitHub Pages'te sınırlı olabilir.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.body.appendChild(notification);
            
            // Initialize basic theme toggle
            const themeToggle = document.getElementById('theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
                    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                    document.documentElement.setAttribute('data-theme', newTheme);
                    localStorage.setItem('risko-theme', newTheme);
                });
            }
        }
    }
    
    initializeWhenReady();
    
    // Handle page visibility changes for better performance
    document.addEventListener('visibilitychange', () => {
        if (window.app && document.visibilityState === 'visible') {
            // Refresh data when page becomes visible
            if (window.app.currentPage === 'dashboard') {
                window.app.refreshDashboardData();
            }
        }
    });
});