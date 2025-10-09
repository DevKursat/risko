import pytest
from app.services.risk_calculator import RiskCalculationService


def test_geocode_address():
    """Test address geocoding."""
    service = RiskCalculationService()
    
    # Test Istanbul
    coords = service.geocode_address("Istanbul, Turkey")
    assert coords is not None
    lat, lon = coords
    assert 40.0 < lat < 42.0  # Istanbul latitude range
    assert 28.0 < lon < 30.0  # Istanbul longitude range
    
    # Test Ankara
    coords = service.geocode_address("Ankara, Turkey")
    assert coords is not None
    lat, lon = coords
    assert 39.0 < lat < 40.5  # Ankara latitude range
    assert 32.0 < lon < 33.5  # Ankara longitude range


def test_earthquake_risk_calculation():
    """Test earthquake risk calculation."""
    service = RiskCalculationService()
    
    # Marmara region should have high earthquake risk
    risk = service.calculate_earthquake_risk(41.0, 29.0)
    assert 60 <= risk <= 100
    
    # Other regions should have lower risk
    risk = service.calculate_earthquake_risk(36.0, 36.0)
    assert 0 <= risk <= 100


def test_flood_risk_calculation():
    """Test flood risk calculation."""
    service = RiskCalculationService()
    
    risk = service.calculate_flood_risk(41.0, 29.0)
    assert 0 <= risk <= 100


def test_fire_risk_calculation():
    """Test fire risk calculation."""
    service = RiskCalculationService()
    
    # Test without building age
    risk = service.calculate_fire_risk(41.0, 29.0)
    assert 0 <= risk <= 100
    
    # Test with old building
    risk_old = service.calculate_fire_risk(41.0, 29.0, building_age=60)
    
    # Test with newer building
    risk_new = service.calculate_fire_risk(41.0, 29.0, building_age=10)
    
    # Older buildings should have higher risk
    assert risk_old >= risk_new


def test_landslide_risk_calculation():
    """Test landslide risk calculation."""
    service = RiskCalculationService()
    
    risk = service.calculate_landslide_risk(41.0, 29.0)
    assert 0 <= risk <= 100


def test_overall_risk_calculation():
    """Test overall risk calculation."""
    service = RiskCalculationService()
    
    # Test with known values
    overall = service.calculate_overall_risk(80, 60, 40, 20)
    
    # Should be weighted average
    expected = (80 * 0.4) + (60 * 0.25) + (40 * 0.2) + (20 * 0.15)
    assert abs(overall - expected) < 0.01


def test_risk_level_classification():
    """Test risk level classification."""
    service = RiskCalculationService()
    
    assert service.get_risk_level(10) == "low"
    assert service.get_risk_level(30) == "medium"
    assert service.get_risk_level(60) == "high"
    assert service.get_risk_level(85) == "critical"


def test_analyze_address():
    """Test complete address analysis."""
    service = RiskCalculationService()
    
    result = service.analyze_address("Istanbul, Turkey", building_age=50)
    
    # Check required fields
    assert "address" in result
    assert "latitude" in result
    assert "longitude" in result
    assert "earthquake_risk" in result
    assert "flood_risk" in result
    assert "fire_risk" in result
    assert "landslide_risk" in result
    assert "overall_risk_score" in result
    assert "risk_level" in result
    assert "building_age" in result
    
    # Check values are valid
    assert result["building_age"] == 50
    assert 0 <= result["earthquake_risk"] <= 100
    assert 0 <= result["flood_risk"] <= 100
    assert 0 <= result["fire_risk"] <= 100
    assert 0 <= result["landslide_risk"] <= 100
    assert 0 <= result["overall_risk_score"] <= 100
    assert result["risk_level"] in ["low", "medium", "high", "critical"]
