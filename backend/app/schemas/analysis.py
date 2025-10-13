from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class AnalysisBase(BaseModel):
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    earthquake_risk: float = Field(..., ge=0, le=100)
    flood_risk: float = Field(..., ge=0, le=100)
    fire_risk: float = Field(..., ge=0, le=100)
    landslide_risk: float = Field(..., ge=0, le=100)
    overall_risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    preventive_actions: Optional[str] = None
    risk_factors_detail: Optional[str] = None
    insurance_guideline: Optional[str] = None


class AnalysisCreate(AnalysisBase):
    owner_id: str


class Analysis(AnalysisBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: str
    created_at: datetime
