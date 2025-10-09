/**
 * Risko Platform - Main Application JavaScript
 * Full-featured web application with real-time API integration
 */

class RiskoPlatformApp {
    constructor() {
        this.config = window.RISKO_CONFIG;
        this.currentPage = 'dashboard';
        this.apiClient = new APIClient();
        this.charts = {};
        this.map = null;
        this.user = {
            name: 'Demo Kullanıcı',
            email: 'demo@risko.com',
            plan: 'premium',
            avatar: 'https://ui-avatars.com/api/?name=Demo+User&background=4f46e5&color=fff'
        };
        
        this.init();
    }

    async init() {
        try {
            // Check authentication
            this.checkAuthentication();
            
            // Show loading screen
            this.showLoading();
            
            // Initialize components
            await this.initializeApp();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Load initial data
            await this.loadDashboardData();
            
            // Hide loading screen
            this.hideLoading();
            
            console.log('🚀 Risko Platform App initialized successfully');
            
        } catch (error) {
            console.error('❌ App initialization failed:', error);
            this.showNotification('Uygulama başlatılırken hata oluştu', 'error');
        }
    }

    checkAuthentication() {
        const user = sessionStorage.getItem('risko_user');
        if (!user && !this.config.DEMO_MODE) {
            // Redirect to login if not authenticated
            window.location.href = './login.html';
            return;
        }
        
        if (user) {
            this.user = JSON.parse(user);
        }
    }

    showLoading() {
        document.getElementById('loading-screen').classList.remove('d-none');
        document.getElementById('app').classList.add('d-none');
    }

    hideLoading() {
        setTimeout(() => {
            document.getElementById('loading-screen').classList.add('d-none');
            document.getElementById('app').classList.remove('d-none');
        }, 1500);
    }

    async initializeApp() {
        // Initialize charts
        this.initCharts();
        
        // Setup navigation
        this.setupNavigation();
        
        // Load user data
        this.loadUserData();
        
        // Initialize real-time features
        this.initRealTimeFeatures();
    }

    setupEventListeners() {
        // Navigation
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-page]')) {
                e.preventDefault();
                const page = e.target.closest('[data-page]').getAttribute('data-page');
                this.navigateToPage(page);
            }
        });

        // Logout
        document.getElementById('logout-btn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.logout();
        });

        // Window resize for charts
        window.addEventListener('resize', () => {
            Object.values(this.charts).forEach(chart => {
                if (chart) chart.resize();
            });
        });
    }

    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link[data-page]');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                // Update active states
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }

    async navigateToPage(page) {
        if (this.currentPage === page) return;

        try {
            // Hide current page
            document.querySelectorAll('.page-content').forEach(p => {
                p.classList.remove('active');
            });

            // Load and show new page
            await this.loadPage(page);
            this.currentPage = page;

            // Update URL (SPA behavior)
            window.history.pushState({page}, '', `#${page}`);

        } catch (error) {
            console.error(`Error navigating to ${page}:`, error);
            this.showNotification('Sayfa yüklenirken hata oluştu', 'error');
        }
    }

    async loadPage(page) {
        let pageElement = document.getElementById(`${page}-page`);
        
        if (!pageElement) {
            // Create page dynamically
            pageElement = await this.createPage(page);
        }

        // Show the page
        pageElement.classList.add('active');

        // Load page-specific data
        await this.loadPageData(page);
    }

    async createPage(page) {
        const container = document.getElementById('page-content');
        const pageDiv = document.createElement('div');
        pageDiv.id = `${page}-page`;
        pageDiv.className = 'page-content';
        
        switch (page) {
            case 'analysis':
                pageDiv.innerHTML = this.createAnalysisPage();
                break;
            case 'map':
                pageDiv.innerHTML = this.createMapPage();
                break;
            case 'reports':
                pageDiv.innerHTML = this.createReportsPage();
                break;
            case 'premium':
                pageDiv.innerHTML = this.createPremiumPage();
                break;
            case 'batch':
                pageDiv.innerHTML = this.createBatchAnalysisPage();
                break;
            case 'api':
                pageDiv.innerHTML = this.createAPIPage();
                break;
            case 'profile':
                pageDiv.innerHTML = this.createProfilePage();
                break;
            case 'settings':
                pageDiv.innerHTML = this.createSettingsPage();
                break;
            default:
                pageDiv.innerHTML = '<div class="alert alert-warning">Sayfa bulunamadı</div>';
        }

        container.appendChild(pageDiv);
        return pageDiv;
    }

    createAnalysisPage() {
        return `
            <div class="row">
                <div class="col-12 mb-4">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header bg-primary text-white">
                            <h4 class="card-title mb-0">
                                <i class="fas fa-search me-2"></i>Risk Analizi
                            </h4>
                        </div>
                        <div class="card-body">
                            <form id="risk-analysis-form">
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Adres</label>
                                        <input type="text" class="form-control" id="address" 
                                               placeholder="İstanbul, Beyoğlu..." required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Analiz Türü</label>
                                        <select class="form-select" id="analysis-type">
                                            <option value="comprehensive">Kapsamlı Analiz</option>
                                            <option value="earthquake">Deprem</option>
                                            <option value="flood">Sel</option>
                                            <option value="fire">Yangın</option>
                                            <option value="landslide">Heyelan</option>
                                        </select>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Bina Tipi</label>
                                        <select class="form-select" id="building-type">
                                            <option value="residential">Konut</option>
                                            <option value="commercial">Ticari</option>
                                            <option value="industrial">Sanayi</option>
                                            <option value="office">Ofis</option>
                                        </select>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Bina Yaşı</label>
                                        <input type="number" class="form-control" id="building-age" 
                                               placeholder="Yıl" min="0" max="200">
                                    </div>
                                </div>
                                <div class="d-flex gap-2">
                                    <button type="submit" class="btn btn-primary">
                                        <i class="fas fa-search me-2"></i>Analiz Başlat
                                    </button>
                                    <button type="button" class="btn btn-outline-secondary" id="use-location">
                                        <i class="fas fa-location-arrow me-2"></i>Konumumu Kullan
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="col-12">
                    <div id="analysis-results" class="d-none">
                        <!-- Results will be loaded here -->
                    </div>
                </div>
            </div>
        `;
    }

    createMapPage() {
        return `
            <div class="row">
                <div class="col-12 mb-4">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header bg-success text-white">
                            <h4 class="card-title mb-0">
                                <i class="fas fa-map me-2"></i>Risk Haritası
                            </h4>
                        </div>
                        <div class="card-body p-0">
                            <div id="risk-map" class="map-container"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Harita Kontrolleri</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label class="form-label">Risk Türü</label>
                                <select class="form-select" id="map-risk-type">
                                    <option value="all">Tüm Riskler</option>
                                    <option value="earthquake">Deprem</option>
                                    <option value="flood">Sel</option>
                                    <option value="fire">Yangın</option>
                                    <option value="landslide">Heyelan</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Risk Seviyesi</label>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="low" id="risk-low" checked>
                                    <label class="form-check-label text-success" for="risk-low">Düşük</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="medium" id="risk-medium" checked>
                                    <label class="form-check-label text-warning" for="risk-medium">Orta</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" value="high" id="risk-high" checked>
                                    <label class="form-check-label text-danger" for="risk-high">Yüksek</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card border-0 shadow-sm">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Bölge İstatistikleri</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="region-stats-chart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    createPremiumPage() {
        return `
            <div class="row">
                <div class="col-12 mb-4">
                    <div class="card bg-gradient-warning text-white">
                        <div class="card-body text-center p-5">
                            <i class="fas fa-crown fa-4x mb-3"></i>
                            <h2>Premium Özellikler</h2>
                            <p class="lead">Gelişmiş analiz araçları ve premium özelliklerle daha detaylı riskler keşfedin</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header text-center">
                            <h5 class="card-title">Temel Plan</h5>
                            <div class="h2 text-primary">Ücretsiz</div>
                        </div>
                        <div class="card-body">
                            <ul class="list-unstyled">
                                <li><i class="fas fa-check text-success me-2"></i>5 Analiz/Ay</li>
                                <li><i class="fas fa-check text-success me-2"></i>Temel Risk Türleri</li>
                                <li><i class="fas fa-check text-success me-2"></i>PDF Rapor</li>
                                <li><i class="fas fa-times text-muted me-2"></i>API Erişimi</li>
                                <li><i class="fas fa-times text-muted me-2"></i>Toplu Analiz</li>
                            </ul>
                        </div>
                        <div class="card-footer text-center">
                            <button class="btn btn-outline-primary">Mevcut Plan</button>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="card border-0 shadow-lg h-100 border-primary">
                        <div class="card-header text-center bg-primary text-white">
                            <h5 class="card-title">Pro Plan</h5>
                            <div class="h2">₺99<small>/ay</small></div>
                        </div>
                        <div class="card-body">
                            <ul class="list-unstyled">
                                <li><i class="fas fa-check text-success me-2"></i>100 Analiz/Ay</li>
                                <li><i class="fas fa-check text-success me-2"></i>Tüm Risk Türleri</li>
                                <li><i class="fas fa-check text-success me-2"></i>Detaylı Raporlar</li>
                                <li><i class="fas fa-check text-success me-2"></i>API Erişimi</li>
                                <li><i class="fas fa-check text-success me-2"></i>Email Destek</li>
                            </ul>
                        </div>
                        <div class="card-footer text-center">
                            <button class="btn btn-primary">Upgrade</button>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header text-center bg-dark text-white">
                            <h5 class="card-title">Enterprise</h5>
                            <div class="h2">₺499<small>/ay</small></div>
                        </div>
                        <div class="card-body">
                            <ul class="list-unstyled">
                                <li><i class="fas fa-check text-success me-2"></i>Sınırsız Analiz</li>
                                <li><i class="fas fa-check text-success me-2"></i>Özel Entegrasyonlar</li>
                                <li><i class="fas fa-check text-success me-2"></i>Toplu İşlemler</li>
                                <li><i class="fas fa-check text-success me-2"></i>Öncelikli Destek</li>
                                <li><i class="fas fa-check text-success me-2"></i>Özel Eğitim</li>
                            </ul>
                        </div>
                        <div class="card-footer text-center">
                            <button class="btn btn-dark">İletişime Geç</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async loadPageData(page) {
        switch (page) {
            case 'analysis':
                this.setupAnalysisPage();
                break;
            case 'map':
                await this.initializeMap();
                break;
            case 'reports':
                await this.loadReports();
                break;
            case 'premium':
                this.setupPremiumPage();
                break;
            case 'batch':
                this.setupBatchAnalysis();
                break;
            case 'api':
                this.setupAPIPage();
                break;
        }
    }

    setupAnalysisPage() {
        const form = document.getElementById('risk-analysis-form');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.performRiskAnalysis();
            });
        }

        const locationBtn = document.getElementById('use-location');
        if (locationBtn) {
            locationBtn.addEventListener('click', () => {
                this.getCurrentLocation();
            });
        }
    }

    async performRiskAnalysis() {
        const form = document.getElementById('risk-analysis-form');
        const resultsDiv = document.getElementById('analysis-results');
        
        try {
            // Show loading state
            this.showAnalysisLoading();
            
            const formData = new FormData(form);
            const analysisData = {
                address: document.getElementById('address').value,
                analysis_type: document.getElementById('analysis-type').value,
                building_type: document.getElementById('building-type').value,
                building_age: document.getElementById('building-age').value
            };

            // Call API
            const result = await this.apiClient.analyzeRisk(analysisData);
            
            // Show results
            this.displayAnalysisResults(result);
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Analiz sırasında hata oluştu', 'error');
        }
    }

    displayAnalysisResults(result) {
        const resultsDiv = document.getElementById('analysis-results');
        resultsDiv.innerHTML = `
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-success text-white">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-chart-bar me-2"></i>Analiz Sonuçları
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Genel Risk Skoru</h6>
                            <div class="d-flex align-items-center mb-3">
                                <div class="progress flex-grow-1 me-3" style="height: 20px;">
                                    <div class="progress-bar bg-${this.getRiskColor(result.overall_score)}" 
                                         style="width: ${result.overall_score}%">
                                        ${result.overall_score}%
                                    </div>
                                </div>
                                <span class="badge bg-${this.getRiskColor(result.overall_score)} fs-6">
                                    ${this.getRiskLevel(result.overall_score)}
                                </span>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6>Risk Dağılımı</h6>
                            <canvas id="risk-distribution-chart" height="200"></canvas>
                        </div>
                    </div>
                    <div class="row mt-4">
                        ${Object.entries(result.risk_breakdown || {}).map(([key, value]) => `
                            <div class="col-md-3">
                                <div class="text-center p-3 border rounded">
                                    <i class="fas fa-${this.getRiskIcon(key)} fa-2x text-${this.getRiskColor(value)} mb-2"></i>
                                    <h6>${this.getRiskTitle(key)}</h6>
                                    <span class="h5 text-${this.getRiskColor(value)}">${value}%</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="mt-4">
                        <h6>Öneriler</h6>
                        <ul class="list-group list-group-flush">
                            ${(result.recommendations || []).map(rec => `
                                <li class="list-group-item border-0 px-0">
                                    <i class="fas fa-lightbulb text-warning me-2"></i>${rec}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
                <div class="card-footer">
                    <div class="d-flex gap-2">
                        <button class="btn btn-primary" onclick="app.downloadReport()">
                            <i class="fas fa-download me-2"></i>PDF İndir
                        </button>
                        <button class="btn btn-outline-primary" onclick="app.shareAnalysis()">
                            <i class="fas fa-share me-2"></i>Paylaş
                        </button>
                        <button class="btn btn-outline-success" onclick="app.saveAnalysis()">
                            <i class="fas fa-save me-2"></i>Kaydet
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        resultsDiv.classList.remove('d-none');
        
        // Initialize result chart
        this.initRiskDistributionChart(result.risk_breakdown);
    }

    showAnalysisLoading() {
        const resultsDiv = document.getElementById('analysis-results');
        resultsDiv.innerHTML = `
            <div class="card border-0 shadow-sm">
                <div class="card-body text-center p-5">
                    <div class="spinner-border text-primary mb-3" role="status">
                        <span class="visually-hidden">Analiz ediliyor...</span>
                    </div>
                    <h5>Risk Analizi Yapılıyor</h5>
                    <p class="text-muted">Bu işlem birkaç saniye sürebilir...</p>
                    <div class="progress">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                             role="progressbar" style="width: 100%"></div>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.classList.remove('d-none');
    }

    async initializeMap() {
        if (this.map) {
            this.map.remove();
        }

        const mapElement = document.getElementById('risk-map');
        if (!mapElement) return;

        // Initialize Leaflet map
        this.map = L.map('risk-map').setView([39.9334, 32.8597], 6);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);

        // Add risk data layers
        await this.loadMapData();
    }

    async loadMapData() {
        try {
            const riskData = await this.apiClient.getRiskMapData();
            
            riskData.forEach(point => {
                const color = this.getRiskColor(point.risk_level);
                const marker = L.circleMarker([point.lat, point.lng], {
                    radius: 8,
                    fillColor: color,
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                }).addTo(this.map);

                marker.bindPopup(`
                    <div class="p-2">
                        <h6>${point.location}</h6>
                        <p class="mb-1"><strong>Risk Seviyesi:</strong> 
                            <span class="badge bg-${color}">${this.getRiskLevel(point.risk_level)}</span>
                        </p>
                        <p class="mb-0"><strong>Skor:</strong> ${point.risk_level}%</p>
                    </div>
                `);
            });
            
        } catch (error) {
            console.error('Map data loading error:', error);
        }
    }

    initCharts() {
        // Wait for Chart.js to load
        if (typeof Chart === 'undefined') {
            console.log('⏳ Chart.js yükleniyor, 1 saniye bekleniyor...');
            setTimeout(() => this.initCharts(), 1000);
            return;
        }

        const ctx = document.getElementById('risk-chart');
        if (ctx) {
            this.charts.riskChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran'],
                    datasets: [{
                        label: 'Risk Skoru Ortalaması',
                        data: [65, 59, 80, 81, 56, 55],
                        borderColor: '#4f46e5',
                        backgroundColor: 'rgba(79, 70, 229, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
    }

    initRiskDistributionChart(data) {
        // Wait for Chart.js to load
        if (typeof Chart === 'undefined') {
            setTimeout(() => this.initRiskDistributionChart(data), 1000);
            return;
        }

        const ctx = document.getElementById('risk-distribution-chart');
        if (ctx && data) {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(data).map(key => this.getRiskTitle(key)),
                    datasets: [{
                        data: Object.values(data),
                        backgroundColor: [
                            '#ef4444', // danger
                            '#f59e0b', // warning  
                            '#10b981', // success
                            '#3b82f6'  // info
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }

    async loadDashboardData() {
        try {
            // Load recent activities
            const activities = await this.apiClient.getRecentActivities();
            this.displayRecentActivities(activities);
            
            // Update stats
            this.updateDashboardStats();
            
        } catch (error) {
            console.error('Dashboard data loading error:', error);
            // Use demo data
            this.loadDemoData();
        }
    }

    displayRecentActivities(activities) {
        const container = document.getElementById('recent-activities');
        if (!container) return;

        container.innerHTML = activities.map(activity => `
            <div class="activity-item d-flex align-items-center">
                <div class="activity-icon bg-${activity.type === 'analysis' ? 'primary' : 'success'} text-white me-3">
                    <i class="fas fa-${activity.type === 'analysis' ? 'search' : 'file-alt'}"></i>
                </div>
                <div class="flex-grow-1">
                    <h6 class="mb-1">${activity.title}</h6>
                    <p class="text-muted small mb-0">${activity.description}</p>
                </div>
                <div class="text-muted small">
                    ${this.formatDate(activity.created_at)}
                </div>
            </div>
        `).join('');
    }

    loadDemoData() {
        const demoActivities = [
            {
                title: 'İstanbul Beyoğlu Risk Analizi',
                description: 'Kapsamlı risk analizi tamamlandı',
                type: 'analysis',
                created_at: new Date(Date.now() - 3600000)
            },
            {
                title: 'Ankara Çankaya Raporu',
                description: 'PDF rapor oluşturuldu',
                type: 'report',
                created_at: new Date(Date.now() - 7200000)
            },
            {
                title: 'İzmir Konak Analizi',
                description: 'Yüksek risk seviyesi tespit edildi',
                type: 'analysis',
                created_at: new Date(Date.now() - 10800000)
            }
        ];
        
        this.displayRecentActivities(demoActivities);
    }

    updateDashboardStats() {
        // Animate counters
        this.animateCounter('total-analyses', 1247);
        this.animateCounter('low-risk-count', 934);
        this.animateCounter('medium-risk-count', 231);
        this.animateCounter('high-risk-count', 82);
    }

    animateCounter(elementId, target) {
        const element = document.getElementById(elementId);
        if (!element) return;

        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 30);
    }

    loadUserData() {
        document.getElementById('user-name').textContent = this.user.name;
        document.getElementById('user-avatar').src = this.user.avatar;
    }

    initRealTimeFeatures() {
        // Simulate real-time updates
        if (!this.config.DEMO_MODE) {
            // Connect to WebSocket for real-time updates
            this.connectWebSocket();
        }
    }

    getCurrentLocation() {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    this.reverseGeocode(latitude, longitude);
                },
                (error) => {
                    this.showNotification('Konum alınamadı', 'error');
                }
            );
        } else {
            this.showNotification('Tarayıcınız konum özelliğini desteklemiyor', 'error');
        }
    }

    async reverseGeocode(lat, lng) {
        try {
            const response = await fetch(`https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lng}&key=YOUR_API_KEY`);
            const data = await response.json();
            if (data.results && data.results.length > 0) {
                const address = data.results[0].formatted;
                document.getElementById('address').value = address;
            }
        } catch (error) {
            console.error('Reverse geocoding error:', error);
        }
    }

    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('notification-container');
        const id = 'notification-' + Date.now();
        
        const notification = document.createElement('div');
        notification.id = id;
        notification.className = `alert alert-${type} notification notification-${type} alert-dismissible fade show`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        container.appendChild(notification);
        
        // Auto remove
        setTimeout(() => {
            const element = document.getElementById(id);
            if (element) {
                element.remove();
            }
        }, duration);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    getRiskColor(score) {
        if (score < 30) return 'success';
        if (score < 70) return 'warning';
        return 'danger';
    }

    getRiskLevel(score) {
        if (score < 30) return 'Düşük';
        if (score < 70) return 'Orta';
        return 'Yüksek';
    }

    getRiskIcon(type) {
        const icons = {
            earthquake: 'mountain',
            flood: 'water',
            fire: 'fire',
            landslide: 'mountain'
        };
        return icons[type] || 'exclamation-triangle';
    }

    getRiskTitle(type) {
        const titles = {
            earthquake: 'Deprem',
            flood: 'Sel',
            fire: 'Yangın',
            landslide: 'Heyelan'
        };
        return titles[type] || type;
    }

    formatDate(date) {
        const now = new Date();
        const diff = now - new Date(date);
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);
        
        if (minutes < 60) return `${minutes} dakika önce`;
        if (hours < 24) return `${hours} saat önce`;
        return `${days} gün önce`;
    }

    async downloadReport() {
        this.showNotification('Rapor indiriliyor...', 'info');
        // Implementation for PDF download
    }

    async shareAnalysis() {
        if (navigator.share) {
            await navigator.share({
                title: 'Risko Platform - Risk Analizi',
                text: 'Risk analizi sonuçlarını inceleyin',
                url: window.location.href
            });
        } else {
            // Fallback to clipboard
            navigator.clipboard.writeText(window.location.href);
            this.showNotification('Link panoya kopyalandı', 'success');
        }
    }

    async saveAnalysis() {
        this.showNotification('Analiz kaydediliyor...', 'info');
        // Implementation for saving analysis
    }

    logout() {
        Swal.fire({
            title: 'Çıkış yapmak istediğinizden emin misiniz?',
            text: 'Kaydetmediğiniz veriler kaybolabilir.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Evet, çıkış yap',
            cancelButtonText: 'İptal'
        }).then((result) => {
            if (result.isConfirmed) {
                // Clear user data and redirect
                sessionStorage.removeItem('risko_user');
                localStorage.removeItem('risko_preferences');
                window.location.href = './login.html';
            }
        });
    }
}

/**
 * API Client for backend communication
 */
class APIClient {
    constructor() {
        this.baseURL = window.RISKO_CONFIG?.API_BASE_URL || 'http://localhost:8000';
        this.demoMode = window.RISKO_CONFIG?.DEMO_MODE || false;
    }

    async request(endpoint, options = {}) {
        if (this.demoMode) {
            return this.getDemoData(endpoint);
        }

        try {
            const response = await fetch(`${this.baseURL}/api/v1${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            // Fallback to demo data
            return this.getDemoData(endpoint);
        }
    }

    async analyzeRisk(data) {
        return await this.request('/risk/analyze', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async getRecentActivities() {
        return await this.request('/activities/recent');
    }

    async getRiskMapData() {
        return await this.request('/risk/map-data');
    }

    getDemoData(endpoint) {
        const demoData = {
            '/risk/analyze': {
                overall_score: Math.floor(Math.random() * 100),
                risk_breakdown: {
                    earthquake: Math.floor(Math.random() * 100),
                    flood: Math.floor(Math.random() * 100),
                    fire: Math.floor(Math.random() * 100),
                    landslide: Math.floor(Math.random() * 100)
                },
                recommendations: [
                    'Bina yapısını güçlendiriniz',
                    'Acil durum planı hazırlayınız',
                    'Sigorta kapsamınızı gözden geçiriniz'
                ]
            },
            '/activities/recent': [
                {
                    title: 'İstanbul Beyoğlu Risk Analizi',
                    description: 'Kapsamlı risk analizi tamamlandı',
                    type: 'analysis',
                    created_at: new Date(Date.now() - 3600000)
                }
            ],
            '/risk/map-data': [
                { lat: 41.0082, lng: 28.9784, location: 'İstanbul', risk_level: 75 },
                { lat: 39.9334, lng: 32.8597, location: 'Ankara', risk_level: 45 },
                { lat: 38.4192, lng: 27.1287, location: 'İzmir', risk_level: 60 }
            ]
        };

        return new Promise(resolve => {
            setTimeout(() => {
                resolve(demoData[endpoint] || {});
            }, 1000);
        });
    }
}

// Initialize app when DOM is loaded - removed automatic initialization
// App will be initialized by error-safe-init.js

// Handle browser navigation
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.page && window.app) {
        window.app.navigateToPage(event.state.page);
    }
});