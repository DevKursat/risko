from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List
from datetime import datetime


class AddressInput(BaseModel):
    address: str = Field(..., description="Full address to analyze")


class RiskScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    earthquake_risk: float = Field(..., ge=0, le=100, description="Earthquake risk score (0-100)")
    flood_risk: float = Field(..., ge=0, le=100, description="Flood risk score (0-100)")
    fire_risk: float = Field(..., ge=0, le=100, description="Fire risk score (0-100)")
    landslide_risk: float = Field(..., ge=0, le=100, description="Landslide risk score (0-100)")
    
    overall_risk_score: float = Field(..., ge=0, le=100, description="Overall risk score (0-100)")
    risk_level: str = Field(..., description="Risk level: low, medium, high, critical")
    
    building_age: Optional[int] = None
    construction_quality: Optional[str] = None


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    risk_type: str
    risk_level: str
    title: str
    description: str
    priority: int


class DetailedRiskReport(BaseModel):
    risk_score: RiskScoreResponse
    recommendations: List[RecommendationResponse]
    analysis: Dict[str, str] = Field(..., description="Detailed analysis for each risk type")
    prevention_tips: List[str] = Field(..., description="General prevention tips")


class RiskVisualization(BaseModel):
    address: str
    risk_map_data: Dict = Field(..., description="GeoJSON data for visualization")
    heat_map_layers: Dict[str, List] = Field(..., description="Heat map layers for different risks")
