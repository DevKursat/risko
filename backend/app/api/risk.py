from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
from app.schemas.risk import (
    AddressInput, 
    RiskScoreResponse, 
    DetailedRiskReport,
    RiskVisualization
)
from app.services.risk_calculator import risk_service
from app.services.recommendations import recommendation_service

router = APIRouter()


# Public endpoints (Freemium)
@router.post("/analyze", response_model=RiskScoreResponse)
async def analyze_address(address_input: AddressInput):
    """
    Analyze risk for a given address (Free tier - basic risk score).
    Returns overall risk score and individual risk scores.
    """
    result = risk_service.analyze_address(address_input.address)
    
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    
    return RiskScoreResponse(**result)


@router.post("/analyze/detailed", response_model=DetailedRiskReport)
async def get_detailed_report(address_input: AddressInput):
    """
    Get detailed risk report with recommendations and analysis (Premium feature).
    Includes personalized recommendations and detailed analysis.
    """
    result = risk_service.analyze_address(address_input.address)
    
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    
    risk_score = RiskScoreResponse(**result)
    
    recommendations = recommendation_service.get_recommendations(
        result['earthquake_risk'],
        result['flood_risk'],
        result['fire_risk'],
        result['landslide_risk']
    )
    
    analysis = recommendation_service.get_analysis(
        result['earthquake_risk'],
        result['flood_risk'],
        result['fire_risk'],
        result['landslide_risk']
    )
    
    prevention_tips = recommendation_service.get_prevention_tips()
    
    return DetailedRiskReport(
        risk_score=risk_score,
        recommendations=recommendations,
        analysis=analysis,
        prevention_tips=prevention_tips
    )


@router.post("/visualize", response_model=RiskVisualization)
async def get_visualization_data(address_input: AddressInput):
    """
    Get risk visualization data for mapping (Premium feature).
    Returns GeoJSON data and heat map layers.
    """
    result = risk_service.analyze_address(address_input.address)
    
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    
    # Create GeoJSON for the location
    risk_map_data = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [result['longitude'], result['latitude']]
            },
            "properties": {
                "address": result['address'],
                "overall_risk": result['overall_risk_score'],
                "risk_level": result['risk_level']
            }
        }]
    }
    
    # Create heat map layers
    heat_map_layers = {
        "earthquake": [{
            "lat": result['latitude'],
            "lon": result['longitude'],
            "intensity": result['earthquake_risk']
        }],
        "flood": [{
            "lat": result['latitude'],
            "lon": result['longitude'],
            "intensity": result['flood_risk']
        }],
        "fire": [{
            "lat": result['latitude'],
            "lon": result['longitude'],
            "intensity": result['fire_risk']
        }],
        "landslide": [{
            "lat": result['latitude'],
            "lon": result['longitude'],
            "intensity": result['landslide_risk']
        }]
    }
    
    return RiskVisualization(
        address=result['address'],
        risk_map_data=risk_map_data,
        heat_map_layers=heat_map_layers
    )
