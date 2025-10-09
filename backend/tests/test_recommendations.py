import pytest
from app.services.recommendations import RecommendationService


def test_get_recommendations():
    """Test recommendation generation."""
    service = RecommendationService()
    
    # Test critical earthquake risk
    recommendations = service.get_recommendations(
        earthquake_risk=80,
        flood_risk=30,
        fire_risk=20,
        landslide_risk=15
    )
    
    assert len(recommendations) > 0
    
    # Should have earthquake recommendations
    earthquake_recs = [r for r in recommendations if r.risk_type == "earthquake"]
    assert len(earthquake_recs) > 0
    
    # Check recommendation structure
    for rec in recommendations:
        assert hasattr(rec, 'id')
        assert hasattr(rec, 'risk_type')
        assert hasattr(rec, 'risk_level')
        assert hasattr(rec, 'title')
        assert hasattr(rec, 'description')
        assert hasattr(rec, 'priority')


def test_recommendations_sorted_by_priority():
    """Test recommendations are sorted by priority."""
    service = RecommendationService()
    
    recommendations = service.get_recommendations(
        earthquake_risk=80,
        flood_risk=80,
        fire_risk=80,
        landslide_risk=80
    )
    
    # Check if sorted by priority
    priorities = [r.priority for r in recommendations]
    assert priorities == sorted(priorities)


def test_get_analysis():
    """Test risk analysis generation."""
    service = RecommendationService()
    
    analysis = service.get_analysis(
        earthquake_risk=80,
        flood_risk=30,
        fire_risk=60,
        landslide_risk=15
    )
    
    # Check all risk types are analyzed
    assert "earthquake" in analysis
    assert "flood" in analysis
    assert "fire" in analysis
    assert "landslide" in analysis
    
    # Check analysis is not empty
    for risk_type, text in analysis.items():
        assert len(text) > 0


def test_analysis_matches_risk_level():
    """Test analysis matches risk levels."""
    service = RecommendationService()
    
    # Critical earthquake risk
    analysis = service.get_analysis(
        earthquake_risk=85,
        flood_risk=20,
        fire_risk=20,
        landslide_risk=20
    )
    
    assert "kritik" in analysis["earthquake"].lower()
    
    # Low flood risk
    analysis = service.get_analysis(
        earthquake_risk=20,
        flood_risk=15,
        fire_risk=20,
        landslide_risk=20
    )
    
    assert "düşük" in analysis["flood"].lower()


def test_get_prevention_tips():
    """Test prevention tips generation."""
    service = RecommendationService()
    
    tips = service.get_prevention_tips()
    
    # Should return multiple tips
    assert len(tips) > 5
    
    # All tips should be strings
    for tip in tips:
        assert isinstance(tip, str)
        assert len(tip) > 0


def test_risk_level_classification():
    """Test internal risk level classification."""
    service = RecommendationService()
    
    assert service._get_risk_level(10) == "low"
    assert service._get_risk_level(30) == "medium"
    assert service._get_risk_level(60) == "high"
    assert service._get_risk_level(85) == "critical"
