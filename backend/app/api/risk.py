from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.risk import (
    AddressInput, 
    RiskScoreResponse, 
    DetailedRiskReport,
    RiskVisualization,
)
from app.schemas.analysis import Analysis as AnalysisResponse, AnalysisCreate
from app.services.risk_calculator import risk_service
from app.services.recommendations import recommendation_service
from app.services.supabase_auth import verify_supabase_jwt
from app.db.session import get_db

router = APIRouter()


# Public endpoints (Freemium)
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_address(
    address_input: AddressInput,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Analyze risk for a given address and persist the analysis to the DB.
    Requires a Supabase JWT in the Authorization header (Bearer <token>).
    Returns the saved Analysis record.
    """

    # Verify token and extract user id
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    token = authorization.split(" ", 1)[1] if authorization.lower().startswith("bearer ") else authorization
    try:
        claims = verify_supabase_jwt(token)
        user_id = claims.get('sub') or claims.get('user_id') or claims.get('aud')
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not user_id:
        raise HTTPException(status_code=401, detail="Unable to determine user id from token")

    # Perform risk analysis
    try:
        result = risk_service.analyze_address(address_input.address)
    except RuntimeError:
        raise HTTPException(status_code=503, detail={"error": "Veri kaynaklarına ulaşılamadı."})
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "Sunucu hatası: analiz gerçekleştirilemedi."})

    if not result or 'error' in result:
        raise HTTPException(status_code=404, detail={"error": "Adres çözümlenemedi veya veri bulunamadı."})

    # Persist to DB (must have owner_id)
    try:
        analysis_in = AnalysisCreate(
            owner_id=user_id,
            address=result.get('address'),
            latitude=result.get('latitude'),
            longitude=result.get('longitude'),
            earthquake_risk=result.get('earthquake_risk'),
            flood_risk=result.get('flood_risk'),
            fire_risk=result.get('fire_risk'),
            landslide_risk=result.get('landslide_risk'),
            overall_risk_score=result.get('overall_risk_score'),
            risk_level=result.get('risk_level'),
        )
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "Analiz verisi doğrulanamadı."})

    try:
        from app.models.analysis import Analysis

        db_obj = Analysis(
            owner_id=analysis_in.owner_id,
            address=analysis_in.address,
            latitude=analysis_in.latitude,
            longitude=analysis_in.longitude,
            earthquake_risk=analysis_in.earthquake_risk,
            flood_risk=analysis_in.flood_risk,
            fire_risk=analysis_in.fire_risk,
            landslide_risk=analysis_in.landslide_risk,
            overall_risk_score=analysis_in.overall_risk_score,
            risk_level=analysis_in.risk_level,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
    except Exception:
        # If DB persistence fails, return server error since storing is required
        raise HTTPException(status_code=500, detail={"error": "Veritabanına kaydedilemedi."})

    # Return the saved analysis
    return AnalysisResponse.from_orm(db_obj)


@router.post("/analyze/detailed", response_model=AnalysisResponse)
async def analyze_detailed(
    address_input: AddressInput,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Perform a detailed premium analysis for a given address and persist the analysis to the DB.
    Requires a Supabase JWT in the Authorization header (Bearer <token>).
    Returns the saved Analysis record with premium fields.
    """

    # Verify token and extract user id
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    token = authorization.split(" ", 1)[1] if authorization.lower().startswith("bearer ") else authorization
    try:
        claims = verify_supabase_jwt(token)
        user_id = claims.get('sub') or claims.get('user_id') or claims.get('aud')
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: user id not found")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    # Calculate standard risk scores
    risk_scores = risk_service.calculate_risk_scores(address_input)

    # Generate premium data
    premium_data = {
        "preventive_actions": '["Temel güçlendirme çalışmaları yapın.", "Acil durum çantası hazırlayın."]',
        "risk_factors_detail": '{"Zemin Sıvılaşması Riski": "Orta", "Fay Hattına Uzaklık": "12km"}',
        "insurance_guideline": "Kapsamlı konut ve deprem sigortası önerilir."
    }

    # Create and save the analysis record
    analysis_data = AnalysisCreate(
        owner_id=user_id,
        address=address_input.address,
        latitude=address_input.latitude,
        longitude=address_input.longitude,
        earthquake_risk=risk_scores.earthquake_risk,
        flood_risk=risk_scores.flood_risk,
        fire_risk=risk_scores.fire_risk,
        landslide_risk=risk_scores.landslide_risk,
        overall_risk_score=risk_scores.overall_risk_score,
        risk_level=risk_scores.risk_level,
        preventive_actions=premium_data["preventive_actions"],
        risk_factors_detail=premium_data["risk_factors_detail"],
        insurance_guideline=premium_data["insurance_guideline"]
    )

    analysis = AnalysisResponse.from_orm(db.add(analysis_data))
    db.commit()
    db.refresh(analysis)

    return analysis


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
