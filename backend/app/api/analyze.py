from fastapi import APIRouter, Depends, HTTPException, Header, Request
from typing import Optional
from app.schemas.risk import AddressInput, RiskScoreResponse
from app.services.risk_calculator import risk_service
from app.services.supabase_auth import verify_supabase_jwt
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.analysis import Analysis
import json

router = APIRouter()


async def _get_user_id(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if not authorization:
        return None
    if authorization.lower().startswith('bearer '):
        token = authorization.split(' ', 1)[1]
    else:
        token = authorization
    try:
        claims = verify_supabase_jwt(token)
        return claims.get('sub') or claims.get('user_id') or claims.get('aud')
    except Exception:
        return None


@router.post('/analyze', response_model=RiskScoreResponse)
async def analyze(address_input: AddressInput, request: Request, user_id: Optional[str] = Depends(_get_user_id), db: Session = Depends(get_db)):
    """Analyze an address and persist the analysis to the analyses table (if DB available)."""
    try:
        result = risk_service.analyze_address(address_input.address, building_age=address_input.building_age)
    except RuntimeError as e:
        # Simulated external API failure or similar
        raise HTTPException(status_code=503, detail={"error": "Veri kaynaklarına ulaşılamadı."})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Sunucu hatası: analiz gerçekleştirilemedi."})

    if not result or 'error' in result:
        # Geocoding failed or no result
        raise HTTPException(status_code=404, detail={"error": "Adres çözümlenemedi veya veri bulunamadı."})

    # Persist to DB (best-effort)
    try:
        analysis = Analysis(
            user_id=user_id,
            address=result.get('address'),
            risk_scores=result
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
    except Exception:
        # Don't fail the request if DB persistence fails; log would be ideal
        pass

    return RiskScoreResponse(**result)
