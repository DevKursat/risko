from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.analysis import Analysis
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
async def analyze_address(address_input: AddressInput, db: Session = Depends(get_db)):
    """
    Analyze risk for a given address (Free tier - basic risk score).
    Returns overall risk score and individual risk scores.
    """
    result = risk_service.analyze_address(address_input.address, address_input.building_age)

    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])

    # Persist analysis to DB (MVP: user_id is None for public analyses)
    try:
        record = Analysis(user_id=None, address=result.get('address') or address_input.address, risk_scores=result)
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception:
        # On DB failure, continue returning result but log is handled by global handler
        pass

    return RiskScoreResponse(**result)


@router.post("/analyze/detailed", response_model=DetailedRiskReport)
async def get_detailed_report(address_input: AddressInput, db: Session = Depends(get_db)):
    """
    Get detailed risk report with recommendations and analysis (Premium feature).
    Includes personalized recommendations and detailed analysis.
    """
    # For MVP premium endpoint: return basic analysis plus a static placeholder message
    result = risk_service.analyze_address(address_input.address, address_input.building_age)

    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])

    # Save to DB
    try:
        record = Analysis(user_id=None, address=result.get('address') or address_input.address, risk_scores=result)
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception:
        pass

    risk_score = RiskScoreResponse(**result)

    # Return a minimal detailed report for now (full premium features coming soon)
    return DetailedRiskReport(
        risk_score=risk_score,
        recommendations=[],
        analysis={"note": "Detaylı rapor ve önleyici analizler yakında bu bölümde yer alacak."},
        prevention_tips=["Detaylı öneriler yakında eklenecek."]
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
