from typing import List, Dict
from app.schemas.risk import RecommendationResponse


class RecommendationService:
    """Service for generating risk-based recommendations."""
    
    def __init__(self):
        self.recommendations_db = {
            'earthquake': {
                'critical': [
                    {
                        'id': 1,
                        'risk_type': 'earthquake',
                        'risk_level': 'critical',
                        'title': 'Bina Güçlendirmesi Acil Gerekli',
                        'description': 'Binanzın deprem dayanıklılığı kritik seviyede düşük. Hemen yapısal güçlendirme yaptırmanızı öneririz.',
                        'priority': 1
                    },
                    {
                        'id': 2,
                        'risk_type': 'earthquake',
                        'risk_level': 'critical',
                        'title': 'Deprem Çantası Hazırlayın',
                        'description': 'Deprem çantası hazırlayın ve güvenli bir noktada saklayın. İçinde su, konserve, ilk yardım malzemeleri bulundurun.',
                        'priority': 2
                    }
                ],
                'high': [
                    {
                        'id': 3,
                        'risk_type': 'earthquake',
                        'risk_level': 'high',
                        'title': 'Yapısal Kontrol Yaptırın',
                        'description': 'Binanızın deprem dayanıklılığını kontrol ettirin. Gerekirse güçlendirme yapın.',
                        'priority': 1
                    }
                ],
                'medium': [
                    {
                        'id': 4,
                        'risk_type': 'earthquake',
                        'risk_level': 'medium',
                        'title': 'Deprem Sigortası Yaptırın',
                        'description': 'DASK deprem sigortası yaptırarak olası zararları minimize edin.',
                        'priority': 2
                    }
                ]
            },
            'flood': {
                'critical': [
                    {
                        'id': 5,
                        'risk_type': 'flood',
                        'risk_level': 'critical',
                        'title': 'Su Baskını Önlemleri Alın',
                        'description': 'Bodrum ve zemin katlarda su yalıtımı yaptırın. Taşkın bariyerleri kurun.',
                        'priority': 1
                    }
                ],
                'high': [
                    {
                        'id': 6,
                        'risk_type': 'flood',
                        'risk_level': 'high',
                        'title': 'Drenaj Sistemi Kontrolü',
                        'description': 'Bina drenaj sistemlerini düzenli kontrol ettirin ve temizletin.',
                        'priority': 2
                    }
                ],
                'medium': [
                    {
                        'id': 7,
                        'risk_type': 'flood',
                        'risk_level': 'medium',
                        'title': 'Yağmur Oluklarını Temizleyin',
                        'description': 'Yağmur olukları ve drenajları düzenli olarak temizleyin.',
                        'priority': 3
                    }
                ]
            },
            'fire': {
                'critical': [
                    {
                        'id': 8,
                        'risk_type': 'fire',
                        'risk_level': 'critical',
                        'title': 'Yangın Alarm Sistemi Kurun',
                        'description': 'Profesyonel yangın alarm ve söndürme sistemi kurdurmanız acil gerekli.',
                        'priority': 1
                    }
                ],
                'high': [
                    {
                        'id': 9,
                        'risk_type': 'fire',
                        'risk_level': 'high',
                        'title': 'Elektrik Tesisatı Yenileyin',
                        'description': 'Eski elektrik tesisatını yenileyin ve yangın sigortası yaptırın.',
                        'priority': 1
                    }
                ],
                'medium': [
                    {
                        'id': 10,
                        'risk_type': 'fire',
                        'risk_level': 'medium',
                        'title': 'Yangın Söndürücü Bulundurun',
                        'description': 'Evde ve ofiste yangın söndürücü bulundurun, kullanımını öğrenin.',
                        'priority': 2
                    }
                ]
            },
            'landslide': {
                'critical': [
                    {
                        'id': 11,
                        'risk_type': 'landslide',
                        'risk_level': 'critical',
                        'title': 'Heyelan Önleme Çalışmaları',
                        'description': 'Acilen heyelan önleme çalışmaları başlatılmalı. İstinat duvarı veya drenaj sistemi gerekli.',
                        'priority': 1
                    }
                ],
                'high': [
                    {
                        'id': 12,
                        'risk_type': 'landslide',
                        'risk_level': 'high',
                        'title': 'Zemin Analizi Yaptırın',
                        'description': 'Zemin ve eğim analizi yaptırarak heyelan riskini değerlendirin.',
                        'priority': 1
                    }
                ],
                'medium': [
                    {
                        'id': 13,
                        'risk_type': 'landslide',
                        'risk_level': 'medium',
                        'title': 'Drenaj Kontrolü',
                        'description': 'Arazideki su akışını kontrol edin ve gerekirse drenaj sistemi kurun.',
                        'priority': 2
                    }
                ]
            }
        }
    
    def get_recommendations(self, earthquake_risk: float, flood_risk: float,
                           fire_risk: float, landslide_risk: float) -> List[RecommendationResponse]:
        """Get recommendations based on risk scores."""
        recommendations = []
        
        risks = {
            'earthquake': earthquake_risk,
            'flood': flood_risk,
            'fire': fire_risk,
            'landslide': landslide_risk
        }
        
        for risk_type, score in risks.items():
            risk_level = self._get_risk_level(score)
            
            if risk_level in self.recommendations_db.get(risk_type, {}):
                recs = self.recommendations_db[risk_type][risk_level]
                for rec in recs:
                    recommendations.append(RecommendationResponse(**rec))
        
        # Sort by priority
        recommendations.sort(key=lambda x: x.priority)
        
        return recommendations
    
    def _get_risk_level(self, score: float) -> str:
        """Convert numeric score to risk level."""
        if score >= 75:
            return 'critical'
        elif score >= 50:
            return 'high'
        elif score >= 25:
            return 'medium'
        else:
            return 'low'
    
    def get_analysis(self, earthquake_risk: float, flood_risk: float,
                     fire_risk: float, landslide_risk: float) -> Dict[str, str]:
        """Get detailed analysis for each risk type."""
        analysis = {}
        
        if earthquake_risk >= 75:
            analysis['earthquake'] = "Bu bölge kritik deprem riski taşımaktadır. Bina güçlendirmesi acil olarak yapılmalıdır."
        elif earthquake_risk >= 50:
            analysis['earthquake'] = "Yüksek deprem riski var. Yapısal kontroller yaptırılmalı."
        elif earthquake_risk >= 25:
            analysis['earthquake'] = "Orta seviye deprem riski mevcut. Önleyici tedbirler alınmalı."
        else:
            analysis['earthquake'] = "Düşük deprem riski. Standart önlemler yeterlidir."
        
        if flood_risk >= 75:
            analysis['flood'] = "Kritik sel/taşkın riski. Su yalıtımı ve drenaj sistemleri acil gerekli."
        elif flood_risk >= 50:
            analysis['flood'] = "Yüksek taşkın riski. Önleyici tedbirler alınmalı."
        elif flood_risk >= 25:
            analysis['flood'] = "Orta seviye taşkın riski. Drenaj kontrolü önerilir."
        else:
            analysis['flood'] = "Düşük taşkın riski. Standart önlemler yeterlidir."
        
        if fire_risk >= 75:
            analysis['fire'] = "Kritik yangın riski. Profesyonel yangın güvenlik sistemleri kurulmalı."
        elif fire_risk >= 50:
            analysis['fire'] = "Yüksek yangın riski. Elektrik tesisatı ve güvenlik önlemleri gözden geçirilmeli."
        elif fire_risk >= 25:
            analysis['fire'] = "Orta seviye yangın riski. Yangın söndürücü ve alarm sistemi önerilir."
        else:
            analysis['fire'] = "Düşük yangın riski. Temel önlemler yeterlidir."
        
        if landslide_risk >= 75:
            analysis['landslide'] = "Kritik heyelan riski. İstinat duvarı ve uzman incelemesi acil gerekli."
        elif landslide_risk >= 50:
            analysis['landslide'] = "Yüksek heyelan riski. Zemin analizi yaptırılmalı."
        elif landslide_risk >= 25:
            analysis['landslide'] = "Orta seviye heyelan riski. Drenaj kontrolü önerilir."
        else:
            analysis['landslide'] = "Düşük heyelan riski. Standart önlemler yeterlidir."
        
        return analysis
    
    def get_prevention_tips(self) -> List[str]:
        """Get general prevention tips."""
        return [
            "Acil durum çantası hazırlayın ve her zaman erişilebilir bir yerde saklayın",
            "Aile afet planı oluşturun ve düzenli olarak tatbikat yapın",
            "Bina sigortalarınızı güncel tutun (DASK ve yangın sigortası)",
            "Acil durum iletişim numaralarını kaydedin ve kolayca erişilebilir yapın",
            "Komşularınızla afet durumunda yardımlaşma planı yapın",
            "Düzenli olarak bina kontrolü yaptırın ve gerekli bakımları aksatmayın",
            "Yerel yönetimlerin afet uyarılarını takip edin",
            "İlk yardım eğitimi alın ve temel ekipmanları bulundurun"
        ]


recommendation_service = RecommendationService()
