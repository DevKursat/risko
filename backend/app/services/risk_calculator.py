from typing import Dict, Tuple, Optional
import random
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class RiskCalculationService:
    """Service for calculating risk scores based on various data sources."""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="risko_platform")
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Convert address to latitude and longitude."""
        try:
            location = self.geolocator.geocode(address, timeout=10)
            if location:
                return (location.latitude, location.longitude)
            return None
        except Exception:
            # Fallback to mock coordinates for demonstration
            # In production, use proper geocoding service
            address_lower = address.lower()
            if 'istanbul' in address_lower:
                return (41.0082, 28.9784)
            elif 'ankara' in address_lower:
                return (39.9334, 32.8597)
            elif 'izmir' in address_lower:
                return (38.4237, 27.1428)
            else:
                # Default to Turkey center
                return (39.0, 35.0)
    
    def calculate_earthquake_risk(self, lat: float, lon: float) -> float:
        """
        Calculate earthquake risk based on location.
        In production, this would use real seismic data.
        """
        # Simulated calculation - in production, use real seismic data
        # Turkey's high-risk zones: Marmara, Eastern Anatolia, Western Anatolia
        if 40.0 <= lat <= 41.5 and 27.0 <= lon <= 30.0:  # Marmara region (high risk)
            return random.uniform(70, 95)
        elif 38.0 <= lat <= 40.0:  # Eastern Anatolia
            return random.uniform(60, 85)
        else:
            return random.uniform(20, 60)
    
    def calculate_flood_risk(self, lat: float, lon: float) -> float:
        """
        Calculate flood risk based on location.
        In production, this would use flood maps and elevation data.
        """
        # Simulated calculation - in production, use real flood maps
        # Coastal areas and river basins have higher risk
        if abs(lat - 41.0) < 0.5 and abs(lon - 29.0) < 1.0:  # Near Istanbul coast
            return random.uniform(50, 75)
        return random.uniform(10, 40)
    
    def calculate_fire_risk(self, lat: float, lon: float, building_age: Optional[int] = None) -> float:
        """
        Calculate fire risk based on location and building characteristics.
        In production, this would use climate data, building density, etc.
        """
        base_risk = random.uniform(15, 35)
        
        # Older buildings have higher fire risk
        if building_age and building_age > 50:
            base_risk += 20
        elif building_age and building_age > 30:
            base_risk += 10
        
        return min(base_risk, 100)
    
    def calculate_landslide_risk(self, lat: float, lon: float) -> float:
        """
        Calculate landslide risk based on location.
        In production, this would use topographic data and soil analysis.
        """
        # Simulated calculation - in production, use real topographic data
        # Mountainous regions have higher risk
        if 37.0 <= lat <= 38.5 or 40.5 <= lat <= 42.0:  # Mountainous areas
            return random.uniform(40, 70)
        return random.uniform(5, 30)
    
    def calculate_overall_risk(self, earthquake: float, flood: float, 
                               fire: float, landslide: float) -> float:
        """Calculate weighted overall risk score."""
        # Weights based on severity and frequency
        weights = {
            'earthquake': 0.4,  # Highest weight due to severity
            'flood': 0.25,
            'fire': 0.2,
            'landslide': 0.15
        }
        
        overall = (
            earthquake * weights['earthquake'] +
            flood * weights['flood'] +
            fire * weights['fire'] +
            landslide * weights['landslide']
        )
        
        return round(overall, 2)
    
    def get_risk_level(self, score: float) -> str:
        """Convert numeric score to risk level."""
        if score >= 75:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 25:
            return "medium"
        else:
            return "low"
    
    def analyze_address(self, address: str, building_age: Optional[int] = None) -> Dict:
        """Perform complete risk analysis for an address."""
        coordinates = self.geocode_address(address)
        
        if not coordinates:
            # Return default values if geocoding fails
            return {
                'address': address,
                'latitude': None,
                'longitude': None,
                'earthquake_risk': 0.0,
                'flood_risk': 0.0,
                'fire_risk': 0.0,
                'landslide_risk': 0.0,
                'overall_risk_score': 0.0,
                'risk_level': 'unknown',
                'building_age': building_age,
                'error': 'Could not geocode address'
            }
        
        lat, lon = coordinates
        
        earthquake_risk = self.calculate_earthquake_risk(lat, lon)
        flood_risk = self.calculate_flood_risk(lat, lon)
        fire_risk = self.calculate_fire_risk(lat, lon, building_age)
        landslide_risk = self.calculate_landslide_risk(lat, lon)
        
        overall_risk = self.calculate_overall_risk(
            earthquake_risk, flood_risk, fire_risk, landslide_risk
        )
        
        return {
            'address': address,
            'latitude': lat,
            'longitude': lon,
            'earthquake_risk': round(earthquake_risk, 2),
            'flood_risk': round(flood_risk, 2),
            'fire_risk': round(fire_risk, 2),
            'landslide_risk': round(landslide_risk, 2),
            'overall_risk_score': overall_risk,
            'risk_level': self.get_risk_level(overall_risk),
            'building_age': building_age
        }


risk_service = RiskCalculationService()
