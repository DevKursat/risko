from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional, List
from app.schemas.risk import AddressInput, RiskScoreResponse, DetailedRiskReport
from app.services.risk_calculator import risk_service
from app.services.recommendations import recommendation_service
from app.core.config import settings

router = APIRouter()


# API key validation with proper settings integration
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key for B2B access."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    # Check against configured API keys
    if x_api_key not in settings.B2B_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return x_api_key


@router.post("/batch-analyze", response_model=List[RiskScoreResponse])
async def batch_analyze(
    addresses: List[AddressInput],
    api_key: str = Depends(verify_api_key)
):
    """
    Batch analysis for multiple addresses (B2B API).
    For insurance companies and banks to analyze multiple properties.
    """
    if len(addresses) > 100:  # Limit batch size
        raise HTTPException(status_code=400, detail="Batch size cannot exceed 100 addresses")
    
    results = []
    
    for address_input in addresses:
        result = risk_service.analyze_address(address_input.address)
        if 'error' not in result:
            results.append(RiskScoreResponse(**result))
    
    return results


@router.post("/premium-analyze", response_model=DetailedRiskReport)
async def premium_analyze(
    address_input: AddressInput,
    building_age: Optional[int] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Premium analysis with additional parameters (B2B API).
    Includes building age and construction quality assessment.
    """
    result = risk_service.analyze_address(address_input.address, building_age)
    
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


@router.get("/risk-statistics")
async def get_risk_statistics(
    region: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Get aggregated risk statistics for a region (B2B API).
    For insurance companies to understand regional risk patterns.
    """
    # In production, this would query the database for statistics
    return {
        "region": region or "Turkey",
        "average_earthquake_risk": 52.3,
        "average_flood_risk": 28.7,
        "average_fire_risk": 31.5,
        "average_landslide_risk": 24.8,
        "total_analyzed_addresses": 15847,
        "high_risk_percentage": 34.2,
        "critical_risk_percentage": 12.5
    }
