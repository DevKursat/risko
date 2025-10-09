// Simple error-safe initialization
window.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Starting error-safe app initialization...');
    
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
        }
    }
    
    initializeWhenReady();
});