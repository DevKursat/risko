import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_basic_risk_analysis():
    """Test basic risk analysis endpoint."""
    response = client.post(
        "/api/v1/risk/analyze",
        json={"address": "Istanbul, Turkey"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "address" in data
    assert "earthquake_risk" in data
    assert "flood_risk" in data
    assert "fire_risk" in data
    assert "landslide_risk" in data
    assert "overall_risk_score" in data
    assert "risk_level" in data
    
    # Check risk scores are in valid range
    assert 0 <= data["earthquake_risk"] <= 100
    assert 0 <= data["flood_risk"] <= 100
    assert 0 <= data["fire_risk"] <= 100
    assert 0 <= data["landslide_risk"] <= 100
    assert 0 <= data["overall_risk_score"] <= 100
    
    # Check risk level is valid
    assert data["risk_level"] in ["low", "medium", "high", "critical"]


def test_detailed_report():
    """Test detailed risk report endpoint."""
    response = client.post(
        "/api/v1/risk/analyze/detailed",
        json={"address": "Ankara, Turkey"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "risk_score" in data
    assert "recommendations" in data
    assert "analysis" in data
    assert "prevention_tips" in data
    
    # Check recommendations
    assert isinstance(data["recommendations"], list)
    
    # Check analysis
    assert "earthquake" in data["analysis"]
    assert "flood" in data["analysis"]
    assert "fire" in data["analysis"]
    assert "landslide" in data["analysis"]
    
    # Check prevention tips
    assert isinstance(data["prevention_tips"], list)
    assert len(data["prevention_tips"]) > 0


def test_visualization_data():
    """Test risk visualization endpoint."""
    response = client.post(
        "/api/v1/risk/visualize",
        json={"address": "Izmir, Turkey"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "address" in data
    assert "risk_map_data" in data
    assert "heat_map_layers" in data
    
    # Check GeoJSON structure
    assert data["risk_map_data"]["type"] == "FeatureCollection"
    assert "features" in data["risk_map_data"]
    
    # Check heat map layers
    assert "earthquake" in data["heat_map_layers"]
    assert "flood" in data["heat_map_layers"]
    assert "fire" in data["heat_map_layers"]
    assert "landslide" in data["heat_map_layers"]


def test_b2b_batch_analysis():
    """Test B2B batch analysis endpoint."""
    response = client.post(
        "/api/v1/b2b/batch-analyze",
        json=[
            {"address": "Istanbul, Turkey"},
            {"address": "Ankara, Turkey"}
        ],
        headers={"X-API-Key": "demo-api-key-123"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check it returns a list
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Check each item has required fields
    for item in data:
        assert "address" in item
        assert "overall_risk_score" in item
        assert "risk_level" in item


def test_b2b_without_api_key():
    """Test B2B endpoint without API key."""
    response = client.post(
        "/api/v1/b2b/batch-analyze",
        json=[{"address": "Istanbul, Turkey"}]
    )
    assert response.status_code == 401


def test_b2b_risk_statistics():
    """Test B2B risk statistics endpoint."""
    response = client.get(
        "/api/v1/b2b/risk-statistics?region=Istanbul",
        headers={"X-API-Key": "demo-api-key-123"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "region" in data
    assert "average_earthquake_risk" in data
    assert "average_flood_risk" in data
    assert "average_fire_risk" in data
    assert "average_landslide_risk" in data
    assert "total_analyzed_addresses" in data
    assert "high_risk_percentage" in data
    assert "critical_risk_percentage" in data
