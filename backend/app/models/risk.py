from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from geoalchemy2 import Geometry

Base = declarative_base()


class RiskData(Base):
    __tablename__ = "risk_data"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry('POINT'))
    
    # Risk scores (0-100)
    earthquake_risk = Column(Float, default=0.0)
    flood_risk = Column(Float, default=0.0)
    fire_risk = Column(Float, default=0.0)
    landslide_risk = Column(Float, default=0.0)
    
    # Overall risk score
    overall_risk_score = Column(Float, default=0.0)
    
    # Building information
    building_age = Column(Integer, nullable=True)
    construction_quality = Column(String, nullable=True)
    
    # Additional metadata
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    risk_type = Column(String, index=True)  # earthquake, flood, fire, landslide
    risk_level = Column(String)  # low, medium, high, critical
    title = Column(String)
    description = Column(Text)
    priority = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    company_name = Column(String)
    is_active = Column(Boolean, default=True)
    tier = Column(String, default="basic")  # basic, premium, enterprise
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
