from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.analysis import Analysis
from app.services.supabase_auth import verify_supabase_jwt

router = APIRouter()


@router.get('/analyses/me')
def get_my_analyses(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail="Authorization required")
    token = authorization.split(' ', 1)[1]
    try:
        claims = verify_supabase_jwt(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Determine user id from claims
    user_id = claims.get('sub') or claims.get('user_id') or claims.get('aud')
    if not user_id:
        raise HTTPException(status_code=401, detail="User id not found in token")

    records = db.query(Analysis).filter(Analysis.user_id == user_id).order_by(Analysis.created_at.desc()).all()
    # Return simplified list
    result = []
    for r in records:
        rs = r.risk_scores or {}
        result.append({
            'id': r.id,
            'address': r.address,
            'overall_risk_score': rs.get('overall_risk_score'),
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'risk_scores': rs,
        })
    return result
