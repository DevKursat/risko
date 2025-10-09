// Risko Platform Frontend JavaScript
class RiskoPlatform {
    constructor() {
        // API Base URL - configurable for different environments
        this.apiBaseUrl = this.getApiBaseUrl();
        this.isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        this.demoMode = this.shouldUseDemoMode();
        this.init();
    }

    shouldUseDemoMode() {
        // Check config first
        if (window.RISKO_CONFIG && window.RISKO_CONFIG.DEMO_MODE) {
            return true;
        }
        
        // Check for GitHub Pages
        if (window.location.hostname.includes('github.io')) {
            return true;
        }
        
        // Check localStorage
        if (localStorage.getItem('risko-demo-mode') === 'true') {
            return true;
        }
        
        // Default for localhost
        return this.isLocalhost;
    }

    getApiBaseUrl() {
        // Use config if available
        if (window.RISKO_CONFIG && window.RISKO_CONFIG.API_BASE_URL) {
            return window.RISKO_CONFIG.API_BASE_URL;
        }
        
        // Check for environment-specific API URL
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8000/api/v1';
        }
        
        // Default fallback for GitHub Pages
        return 'https://risko-api.herokuapp.com/api/v1'; // Change this!
    }

    init() {
        this.bindEvents();
        this.initScrollEffects();
    }

    bindEvents() {
        // Form submission
        document.getElementById('riskForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.analyzeRisk();
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }

    initScrollEffects() {
        // Navbar background on scroll
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            }
        });
    }

    async analyzeRisk() {
        const address = document.getElementById('address').value;
        const buildingAge = document.getElementById('buildingAge').value;
        const analysisType = document.getElementById('analysisType').value;

        if (!address.trim()) {
            this.showAlert('Lütfen bir adres giriniz.', 'warning');
            return;
        }

        this.showLoading(true);
        this.hideResults();

        try {
            // Check if we should use demo mode
            if (this.demoMode) {
                console.log('Using demo mode - mock data');
                await this.handleDemoMode(address, analysisType);
                return;
            }

            let url, data;
            
            if (analysisType === 'detailed') {
                url = `${this.apiBaseUrl}/risk/analyze/detailed`;
                data = { address };
            } else {
                url = `${this.apiBaseUrl}/risk/analyze`;
                data = { address };
            }

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (analysisType === 'detailed') {
                this.displayDetailedResults(result);
            } else {
                this.displayBasicResults(result);
            }

            Analytics.trackEvent('Analysis', 'Complete', analysisType);

        } catch (error) {
            console.error('API Error:', error);
            
            // Fallback to demo mode if API fails
            if (!this.demoMode) {
                this.showAlert('API\'ye bağlanılamıyor. Demo modu aktif ediliyor...', 'info');
                await this.handleDemoMode(address, analysisType);
                return;
            }
            
            this.showAlert('Analiz sırasında bir hata oluştu. Lütfen tekrar deneyin.', 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    async handleDemoMode(address, analysisType) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        let result;
        if (analysisType === 'detailed') {
            result = DemoData.getDetailedAnalysis(address);
            this.displayDetailedResults(result);
        } else {
            result = DemoData.getRiskAnalysis(address);
            this.displayBasicResults(result);
        }

        Analytics.trackEvent('Analysis', 'Demo', analysisType);
    }

    displayBasicResults(data) {
        this.displayRiskScores(data);
        this.displayLocationInfo(data);
        this.showResults();
    }

    displayDetailedResults(data) {
        this.displayRiskScores(data.risk_score);
        this.displayLocationInfo(data.risk_score);
        this.displayRecommendations(data.recommendations, data.analysis);
        this.showResults();
    }

    displayRiskScores(data) {
        const risksContainer = document.getElementById('riskResults');
        const risks = [
            { name: 'Deprem', key: 'earthquake_risk', icon: 'fas fa-house-crack' },
            { name: 'Sel', key: 'flood_risk', icon: 'fas fa-water' },
            { name: 'Yangın', key: 'fire_risk', icon: 'fas fa-fire' },
            { name: 'Heyelan', key: 'landslide_risk', icon: 'fas fa-mountain' }
        ];

        risksContainer.innerHTML = '';

        risks.forEach(risk => {
            const score = data[risk.key] || 0;
            const level = this.getRiskLevel(score);
            
            const riskCard = document.createElement('div');
            riskCard.className = `risk-card risk-${level}`;
            riskCard.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div class="d-flex align-items-center">
                        <i class="${risk.icon} me-2"></i>
                        <strong>${risk.name} Riski</strong>
                    </div>
                    <span class="badge bg-${this.getRiskBadgeColor(level)}">${this.getRiskLevelText(level)}</span>
                </div>
                <div class="progress mb-2">
                    <div class="progress-bar bg-${this.getRiskColor(level)}" 
                         role="progressbar" 
                         style="width: ${score}%"></div>
                </div>
                <div class="d-flex justify-content-between">
                    <small class="text-muted">Risk Skoru</small>
                    <small class="fw-bold">${score.toFixed(1)}/100</small>
                </div>
            `;
            risksContainer.appendChild(riskCard);
        });

        // Overall risk score
        const overallScore = data.overall_risk_score || 0;
        const overallLevel = this.getRiskLevel(overallScore);
        
        document.getElementById('overallScore').textContent = `${overallScore.toFixed(1)}/100`;
        const progressBar = document.getElementById('overallProgress');
        progressBar.style.width = `${overallScore}%`;
        progressBar.className = `progress-bar bg-${this.getRiskColor(overallLevel)}`;
    }

    displayLocationInfo(data) {
        const coordinates = data.latitude && data.longitude 
            ? `${data.latitude.toFixed(4)}, ${data.longitude.toFixed(4)}`
            : 'Bulunamadı';
        
        document.getElementById('coordinates').textContent = coordinates;
    }

    displayRecommendations(recommendations, analysis) {
        const section = document.getElementById('recommendationsSection');
        const container = document.getElementById('recommendationsList');
        
        container.innerHTML = '';

        if (recommendations && recommendations.length > 0) {
            recommendations.forEach(rec => {
                const recItem = document.createElement('div');
                recItem.className = 'recommendation-item';
                recItem.innerHTML = `
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="mb-0">${rec.title}</h6>
                        <span class="badge bg-${this.getPriorityColor(rec.priority)}">
                            Öncelik ${rec.priority}
                        </span>
                    </div>
                    <p class="mb-1 text-muted">${rec.description}</p>
                    <small class="text-primary">
                        <i class="fas fa-tag"></i> ${rec.risk_type} - ${rec.risk_level}
                    </small>
                `;
                container.appendChild(recItem);
            });
        }

        if (analysis) {
            Object.entries(analysis).forEach(([riskType, analysisText]) => {
                const analysisItem = document.createElement('div');
                analysisItem.className = 'recommendation-item border-start border-info';
                analysisItem.innerHTML = `
                    <h6><i class="fas fa-chart-line me-2"></i>${this.getRiskTypeText(riskType)} Analizi</h6>
                    <p class="mb-0 text-muted">${analysisText}</p>
                `;
                container.appendChild(analysisItem);
            });
        }

        section.style.display = 'block';
    }

    getRiskLevel(score) {
        if (score >= 75) return 'critical';
        if (score >= 50) return 'high';
        if (score >= 25) return 'medium';
        return 'low';
    }

    getRiskLevelText(level) {
        const levels = {
            'low': 'Düşük',
            'medium': 'Orta',
            'high': 'Yüksek',
            'critical': 'Kritik'
        };
        return levels[level] || 'Bilinmiyor';
    }

    getRiskColor(level) {
        const colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger',
            'critical': 'dark'
        };
        return colors[level] || 'secondary';
    }

    getRiskBadgeColor(level) {
        const colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger',
            'critical': 'dark'
        };
        return colors[level] || 'secondary';
    }

    getPriorityColor(priority) {
        if (priority === 1) return 'danger';
        if (priority === 2) return 'warning';
        return 'info';
    }

    getRiskTypeText(riskType) {
        const types = {
            'earthquake': 'Deprem',
            'flood': 'Sel',
            'fire': 'Yangın',
            'landslide': 'Heyelan'
        };
        return types[riskType] || riskType;
    }

    showLoading(show) {
        const loading = document.querySelector('.loading');
        if (show) {
            loading.classList.add('show');
        } else {
            loading.classList.remove('show');
        }
    }

    showResults() {
        const results = document.querySelector('.result-section');
        results.classList.add('show');
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    hideResults() {
        const results = document.querySelector('.result-section');
        results.classList.remove('show');
        
        const recommendations = document.getElementById('recommendationsSection');
        recommendations.style.display = 'none';
    }

    showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert after form
        const form = document.getElementById('riskForm');
        form.parentNode.insertBefore(alertDiv, form.nextSibling);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Demo data for testing without backend
class DemoData {
    static getRiskAnalysis(address) {
        return {
            address: address,
            latitude: 41.0082 + (Math.random() - 0.5) * 0.1,
            longitude: 28.9784 + (Math.random() - 0.5) * 0.1,
            earthquake_risk: Math.random() * 100,
            flood_risk: Math.random() * 100,
            fire_risk: Math.random() * 100,
            landslide_risk: Math.random() * 100,
            overall_risk_score: Math.random() * 100,
            risk_level: ['low', 'medium', 'high', 'critical'][Math.floor(Math.random() * 4)],
            building_age: null,
            construction_quality: null
        };
    }

    static getDetailedAnalysis(address) {
        const riskScore = this.getRiskAnalysis(address);
        return {
            risk_score: riskScore,
            recommendations: [
                {
                    id: 1,
                    risk_type: 'earthquake',
                    risk_level: 'high',
                    title: 'Bina Güçlendirmesi Önerilir',
                    description: 'Binanızın deprem dayanıklılığını artırmak için yapısal güçlendirme yapılmasını öneririz.',
                    priority: 1
                },
                {
                    id: 2,
                    risk_type: 'flood',
                    risk_level: 'medium',
                    title: 'Su Yalıtımı Kontrolü',
                    description: 'Bodrum ve zemin katların su yalıtımını düzenli olarak kontrol ettirin.',
                    priority: 2
                }
            ],
            analysis: {
                earthquake: 'Bu bölge aktif fay hatlarına yakın konumda bulunmaktadır.',
                flood: 'Yağış miktarları ve drenaj sistemi dikkate alınmalıdır.',
                fire: 'Bina yaşı ve elektrik tesisatı risk faktörleridir.',
                landslide: 'Topografik yapı genel olarak stabildir.'
            },
            prevention_tips: [
                'Deprem çantası hazırlayın',
                'Acil durum planı yapın',
                'Sigorta poliçenizi gözden geçirin'
            ]
        };
    }
}

// Analytics and tracking
class Analytics {
    static trackEvent(category, action, label = '') {
        console.log(`Analytics: ${category} - ${action} - ${label}`);
        // Here you would integrate with Google Analytics, Mixpanel, etc.
    }

    static trackPageView(page) {
        console.log(`Page view: ${page}`);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const app = new RiskoPlatform();
    
    // Track page load
    Analytics.trackPageView('home');
    
    // Add some interactive demo features
    const demoMode = localStorage.getItem('risko-demo-mode') === 'true';
    
    if (demoMode) {
        console.log('Demo mode enabled - using mock data');
        
        // Override API calls with demo data
        RiskoPlatform.prototype.analyzeRisk = async function() {
            const address = document.getElementById('address').value;
            const analysisType = document.getElementById('analysisType').value;

            if (!address.trim()) {
                this.showAlert('Lütfen bir adres giriniz.', 'warning');
                return;
            }

            this.showLoading(true);
            this.hideResults();

            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 2000));

            try {
                let result;
                if (analysisType === 'detailed') {
                    result = DemoData.getDetailedAnalysis(address);
                    this.displayDetailedResults(result);
                } else {
                    result = DemoData.getRiskAnalysis(address);
                    this.displayBasicResults(result);
                }

                Analytics.trackEvent('Analysis', 'Complete', analysisType);
            } catch (error) {
                console.error('Error:', error);
                this.showAlert('Analiz sırasında bir hata oluştu. Lütfen tekrar deneyin.', 'danger');
            } finally {
                this.showLoading(false);
            }
        };
    }
});

// Enable demo mode for development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    localStorage.setItem('risko-demo-mode', 'true');
}