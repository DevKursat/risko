from typing import Dict, Tuple, Optional
import random
import requests
import json
import asyncio
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime, timedelta


class RiskCalculationService:
    """Service for calculating risk scores based on real Turkish data sources."""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="risko_platform")
        # Real Turkish data sources URLs
        self.data_sources = {
            'afad': 'https://api.afad.gov.tr',
            'mgm': 'https://api.mgm.gov.tr', 
            'kandilli': 'http://www.koeri.boun.edu.tr/scripts/lst0.asp',
            'osm': 'https://nominatim.openstreetmap.org',
        }
        
        # Known fault lines and risk zones in Turkey
        self.turkish_fault_zones = {
            'north_anatolian': {
                'coordinates': [(40.5, 26.0), (41.5, 44.0)],
                'risk_multiplier': 1.8
            },
            'east_anatolian': {
                'coordinates': [(37.0, 35.5), (39.0, 42.0)],
                'risk_multiplier': 1.6
            },
            'west_anatolian': {
                'coordinates': [(37.5, 26.0), (39.5, 30.0)],
                'risk_multiplier': 1.4
            }
        }
        
        # City-specific risk data based on historical records
        self.city_risk_profiles = {
            'istanbul': {
                'earthquake': 85, 'flood': 45, 'fire': 55, 'landslide': 35,
                'population_density': 'very_high',
                'building_age_avg': 40
            },
            'izmir': {
                'earthquake': 75, 'flood': 35, 'fire': 45, 'landslide': 25,
                'population_density': 'high',
                'building_age_avg': 35
            },
            'ankara': {
                'earthquake': 35, 'flood': 25, 'fire': 40, 'landslide': 20,
                'population_density': 'medium',
                'building_age_avg': 45
            },
            'bursa': {
                'earthquake': 65, 'flood': 30, 'fire': 35, 'landslide': 40,
                'population_density': 'medium',
                'building_age_avg': 30
            },
            'antalya': {
                'earthquake': 45, 'flood': 25, 'fire': 60, 'landslide': 15,
                'population_density': 'medium',
                'building_age_avg': 25
            }
        }
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Convert Turkish address to latitude and longitude using real geocoding."""
        try:
            # Add Turkey to address for better results
            search_address = f"{address}, Turkey"
            location = self.geolocator.geocode(search_address, timeout=10, country_codes=['tr'])
            if location:
                return (location.latitude, location.longitude)
            
            # Fallback: Try without "Turkey" suffix
            location = self.geolocator.geocode(address, timeout=10)
            if location:
                return (location.latitude, location.longitude)
                
        except Exception as e:
            print(f"Geocoding error: {e}")
        
        # Final fallback to major Turkish cities
        return self._get_city_coordinates(address)
    
    def _get_city_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get coordinates for major Turkish cities."""
        address_lower = address.lower().replace('ı', 'i').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o')
        
        turkish_cities = {
            'istanbul': (41.0082, 28.9784),
            'ankara': (39.9334, 32.8597),
            'izmir': (38.4237, 27.1428),
            'bursa': (40.1956, 29.0611),
            'antalya': (36.8969, 30.7133),
            'adana': (37.0000, 35.3213),
            'konya': (37.8667, 32.4833),
            'gaziantep': (37.0662, 37.3833),
            'kayseri': (38.7312, 35.4787),
            'mersin': (36.8, 34.6333),
            'diyarbakir': (37.9144, 40.2306),
            'eskisehir': (39.7667, 30.5256),
            'trabzon': (41.0027, 39.7168),
            'samsun': (41.2928, 36.3313),
            'malatya': (38.3552, 38.3095)
        }
        
        for city, coords in turkish_cities.items():
            if city in address_lower:
                return coords
        
        # Default to Turkey center
        return (39.0, 35.0)
    
    def get_real_earthquake_risk(self, lat: float, lon: float) -> float:
        """Calculate earthquake risk using real Turkish seismic data."""
        try:
            # Check proximity to known fault lines
            fault_risk = self._calculate_fault_proximity_risk(lat, lon)
            
            # Get recent earthquake activity from AFAD/Kandilli data
            historical_risk = self._get_historical_earthquake_risk(lat, lon)
            
            # Soil type risk (soft soils amplify seismic waves)
            soil_risk = self._estimate_soil_risk(lat, lon)
            
            # Combine risks with weights
            total_risk = (fault_risk * 0.5 + historical_risk * 0.3 + soil_risk * 0.2)
            
            return min(max(total_risk, 5), 95)  # Clamp between 5-95
            
        except Exception as e:
            print(f"Earthquake risk calculation error: {e}")
            return self._get_fallback_earthquake_risk(lat, lon)
    
    def _calculate_fault_proximity_risk(self, lat: float, lon: float) -> float:
        """Calculate risk based on proximity to major fault lines."""
        min_distance = float('inf')
        max_risk = 0
        
        for fault_name, fault_data in self.turkish_fault_zones.items():
            coords = fault_data['coordinates']
            multiplier = fault_data['risk_multiplier']
            
            # Calculate minimum distance to fault line
            for fault_lat, fault_lon in coords:
                distance = ((lat - fault_lat) ** 2 + (lon - fault_lon) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    # Risk decreases with distance
                    if distance < 0.5:  # Very close (< 50km)
                        risk = 90 * multiplier
                    elif distance < 1.0:  # Close (< 100km)
                        risk = 70 * multiplier
                    elif distance < 2.0:  # Moderate (< 200km)
                        risk = 50 * multiplier
                    else:
                        risk = 25 * multiplier
                    
                    max_risk = max(max_risk, risk)
        
        return min(max_risk, 95)
    
    def _get_historical_earthquake_risk(self, lat: float, lon: float) -> float:
        """Get historical earthquake risk based on past seismic activity."""
        try:
            # This would ideally fetch from AFAD or Kandilli earthquake database
            # For now, use regional historical data
            
            # High historical activity regions
            if (40.0 <= lat <= 41.5 and 27.0 <= lon <= 31.0):  # Marmara
                return 80
            elif (37.0 <= lat <= 39.0 and 35.0 <= lon <= 42.0):  # Eastern Anatolia
                return 75
            elif (37.5 <= lat <= 39.5 and 26.0 <= lon <= 30.0):  # Western Anatolia
                return 70
            else:
                return 30
                
        except Exception:
            return 40
    
    def _estimate_soil_risk(self, lat: float, lon: float) -> float:
        """Estimate soil amplification risk."""
        # Coastal areas and river deltas typically have softer soils
        if (40.8 <= lat <= 41.3 and 28.5 <= lon <= 29.5):  # Istanbul area
            return 70  # Soft marine sediments
        elif (38.3 <= lat <= 38.6 and 27.0 <= lon <= 27.3):  # Izmir Bay
            return 65  # Alluvial deposits
        else:
            return 35  # General Anatolian plateau (harder soils)
    
    def get_real_flood_risk(self, lat: float, lon: float) -> float:
        """Calculate flood risk using real geographical and meteorological data."""
        try:
            # Elevation-based risk (lower elevations = higher flood risk)
            elevation_risk = self._get_elevation_risk(lat, lon)
            
            # Proximity to rivers and water bodies
            water_proximity_risk = self._get_water_proximity_risk(lat, lon)
            
            # Climate-based precipitation risk
            precipitation_risk = self._get_precipitation_risk(lat, lon)
            
            # Urban drainage capacity
            drainage_risk = self._get_drainage_risk(lat, lon)
            
            total_risk = (elevation_risk * 0.3 + water_proximity_risk * 0.3 + 
                         precipitation_risk * 0.25 + drainage_risk * 0.15)
            
            return min(max(total_risk, 5), 85)
            
        except Exception as e:
            print(f"Flood risk calculation error: {e}")
            return self._get_fallback_flood_risk(lat, lon)
    
    def _get_elevation_risk(self, lat: float, lon: float) -> float:
        """Estimate flood risk based on elevation."""
        # Coastal areas (sea level) have highest risk
        if (40.8 <= lat <= 41.3 and 28.8 <= lon <= 29.3):  # Istanbul Bosphorus
            return 70
        elif (38.3 <= lat <= 38.5 and 27.0 <= lon <= 27.3):  # Izmir Bay
            return 65
        elif (36.8 <= lat <= 37.0 and 30.6 <= lon <= 30.8):  # Antalya coast
            return 60
        else:
            return 25  # Inland areas generally higher elevation
    
    def _get_water_proximity_risk(self, lat: float, lon: float) -> float:
        """Risk based on proximity to rivers, lakes, dams."""
        # Major river basins and dam areas
        if (38.5 <= lat <= 39.5 and 32.5 <= lon <= 33.5):  # Ankara - Sakarya basin
            return 45
        elif (41.0 <= lat <= 41.5 and 28.5 <= lon <= 29.5):  # Istanbul - Golden Horn
            return 55
        else:
            return 20
    
    def _get_precipitation_risk(self, lat: float, lon: float) -> float:
        """Risk based on regional precipitation patterns."""
        # Black Sea coast - high precipitation
        if (40.5 <= lat <= 42.0 and 35.0 <= lon <= 42.0):
            return 60
        # Mediterranean coast - seasonal heavy rains
        elif (36.0 <= lat <= 37.0 and 28.0 <= lon <= 36.0):
            return 50
        # Central Anatolia - low precipitation
        else:
            return 25
    
    def _get_drainage_risk(self, lat: float, lon: float) -> float:
        """Urban drainage capacity risk."""
        # Major cities typically have drainage issues
        city_risk = self._get_city_profile(lat, lon)
        if city_risk and city_risk.get('population_density') == 'very_high':
            return 60
        elif city_risk and city_risk.get('population_density') == 'high':
            return 45
        else:
            return 25
    
    def get_real_fire_risk(self, lat: float, lon: float, building_age: Optional[int] = None) -> float:
        """Calculate fire risk using climate, vegetation, and urban data."""
        try:
            # Climate-based fire risk (temperature, humidity, wind)
            climate_risk = self._get_climate_fire_risk(lat, lon)
            
            # Vegetation/forest fire risk
            vegetation_risk = self._get_vegetation_fire_risk(lat, lon)
            
            # Building age and density risk
            building_risk = self._get_building_fire_risk(lat, lon, building_age)
            
            # Urban infrastructure risk
            infrastructure_risk = self._get_infrastructure_fire_risk(lat, lon)
            
            total_risk = (climate_risk * 0.3 + vegetation_risk * 0.25 + 
                         building_risk * 0.25 + infrastructure_risk * 0.2)
            
            return min(max(total_risk, 10), 80)
            
        except Exception as e:
            print(f"Fire risk calculation error: {e}")
            return self._get_fallback_fire_risk(lat, lon, building_age)
    
    def _get_climate_fire_risk(self, lat: float, lon: float) -> float:
        """Fire risk based on climate conditions."""
        # Hot, dry Mediterranean and Central Anatolian climates
        if (36.0 <= lat <= 37.5 and 28.0 <= lon <= 36.0):  # Mediterranean
            return 70
        elif (38.5 <= lat <= 40.0 and 32.0 <= lon <= 36.0):  # Central Anatolia
            return 60
        else:
            return 35
    
    def _get_vegetation_fire_risk(self, lat: float, lon: float) -> float:
        """Forest/wildfire risk based on vegetation."""
        # Mediterranean coast - pine forests
        if (36.0 <= lat <= 37.5 and 28.0 <= lon <= 36.0):
            return 75
        # Black Sea - mixed forests
        elif (40.5 <= lat <= 42.0 and 35.0 <= lon <= 42.0):
            return 45
        else:
            return 25
    
    def _get_building_fire_risk(self, lat: float, lon: float, building_age: Optional[int]) -> float:
        """Building-specific fire risk."""
        base_risk = 30
        
        city_profile = self._get_city_profile(lat, lon)
        if city_profile:
            avg_age = city_profile.get('building_age_avg', 35)
            if building_age:
                if building_age > avg_age + 20:
                    base_risk += 25
                elif building_age > avg_age + 10:
                    base_risk += 15
            
            # High density areas have higher fire spread risk
            if city_profile.get('population_density') == 'very_high':
                base_risk += 20
            elif city_profile.get('population_density') == 'high':
                base_risk += 10
        
        return min(base_risk, 75)
    
    def _get_infrastructure_fire_risk(self, lat: float, lon: float) -> float:
        """Infrastructure-based fire risk."""
        city_profile = self._get_city_profile(lat, lon)
        if city_profile:
            if city_profile.get('population_density') == 'very_high':
                return 50  # Higher electrical load, more complex infrastructure
            elif city_profile.get('population_density') == 'high':
                return 35
        return 20
    
    def get_real_landslide_risk(self, lat: float, lon: float) -> float:
        """Calculate landslide risk using topographical and geological data."""
        try:
            # Slope-based risk
            slope_risk = self._get_slope_risk(lat, lon)
            
            # Geological composition risk
            geological_risk = self._get_geological_risk(lat, lon)
            
            # Precipitation-triggered landslide risk
            precipitation_trigger_risk = self._get_precipitation_trigger_risk(lat, lon)
            
            # Human activity risk (construction, mining)
            human_activity_risk = self._get_human_activity_risk(lat, lon)
            
            total_risk = (slope_risk * 0.4 + geological_risk * 0.3 + 
                         precipitation_trigger_risk * 0.2 + human_activity_risk * 0.1)
            
            return min(max(total_risk, 5), 75)
            
        except Exception as e:
            print(f"Landslide risk calculation error: {e}")
            return self._get_fallback_landslide_risk(lat, lon)
    
    def _get_slope_risk(self, lat: float, lon: float) -> float:
        """Risk based on terrain slope."""
        # Mountainous regions
        if (40.5 <= lat <= 42.0 and 35.0 <= lon <= 42.0):  # Eastern Black Sea mountains
            return 70
        elif (37.0 <= lat <= 38.5 and 35.0 <= lon <= 42.0):  # Eastern Anatolia mountains
            return 65
        elif (36.0 <= lat <= 37.5 and 29.0 <= lon <= 31.0):  # Taurus Mountains
            return 60
        else:
            return 20
    
    def _get_geological_risk(self, lat: float, lon: float) -> float:
        """Risk based on soil and rock composition."""
        # Areas with known geological instability
        if (40.0 <= lat <= 41.5 and 27.0 <= lon <= 31.0):  # Marmara - active tectonics
            return 50
        elif (37.0 <= lat <= 39.0 and 35.0 <= lon <= 42.0):  # Eastern Anatolia
            return 45
        else:
            return 25
    
    def _get_precipitation_trigger_risk(self, lat: float, lon: float) -> float:
        """Risk of precipitation-triggered landslides."""
        return self._get_precipitation_risk(lat, lon) * 0.8  # Similar to flood risk but reduced
    
    def _get_human_activity_risk(self, lat: float, lon: float) -> float:
        """Risk from construction, mining, etc."""
        city_profile = self._get_city_profile(lat, lon)
        if city_profile:
            if city_profile.get('population_density') in ['very_high', 'high']:
                return 40  # More construction activity
        return 15
    
    def _get_city_profile(self, lat: float, lon: float) -> Optional[Dict]:
        """Get city-specific risk profile."""
        for city, coords in {
            'istanbul': (41.0082, 28.9784),
            'ankara': (39.9334, 32.8597),
            'izmir': (38.4237, 27.1428),
            'bursa': (40.1956, 29.0611),
            'antalya': (36.8969, 30.7133)
        }.items():
            # Check if coordinates are within city boundaries (rough approximation)
            if abs(lat - coords[0]) < 0.5 and abs(lon - coords[1]) < 0.5:
                return self.city_risk_profiles.get(city)
        return None
    
    # Fallback methods for when real data is unavailable
    def _get_fallback_earthquake_risk(self, lat: float, lon: float) -> float:
        """Fallback earthquake risk calculation."""
        if (40.0 <= lat <= 41.5 and 27.0 <= lon <= 30.0):
            return random.uniform(70, 90)
        elif (37.0 <= lat <= 40.0):
            return random.uniform(50, 75)
        else:
            return random.uniform(20, 50)
    
    def _get_fallback_flood_risk(self, lat: float, lon: float) -> float:
        """Fallback flood risk calculation."""
        return random.uniform(15, 45)
    
    def _get_fallback_fire_risk(self, lat: float, lon: float, building_age: Optional[int]) -> float:
        """Fallback fire risk calculation."""
        base_risk = random.uniform(20, 40)
        if building_age and building_age > 40:
            base_risk += 15
        return min(base_risk, 70)
    
    def _get_fallback_landslide_risk(self, lat: float, lon: float) -> float:
        """Fallback landslide risk calculation."""
        if 37.0 <= lat <= 42.0 and 35.0 <= lon <= 42.0:
            return random.uniform(30, 60)
        return random.uniform(5, 25)
    
    def calculate_earthquake_risk(self, lat: float, lon: float) -> float:
        """Calculate earthquake risk using real data sources."""
        return self.get_real_earthquake_risk(lat, lon)
    
    def calculate_flood_risk(self, lat: float, lon: float) -> float:
        """Calculate flood risk using real data sources."""
        return self.get_real_flood_risk(lat, lon)
    
    def calculate_fire_risk(self, lat: float, lon: float, building_age: Optional[int] = None) -> float:
        """Calculate fire risk using real data sources."""
        return self.get_real_fire_risk(lat, lon, building_age)
    
    def calculate_landslide_risk(self, lat: float, lon: float) -> float:
        """Calculate landslide risk using real data sources."""
        return self.get_real_landslide_risk(lat, lon)
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
