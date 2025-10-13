from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(String, index=True, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    earthquake_risk = Column(Float, nullable=True)
    flood_risk = Column(Float, nullable=True)
    fire_risk = Column(Float, nullable=True)
    landslide_risk = Column(Float, nullable=True)
    overall_risk_score = Column(Float, nullable=True)
    risk_level = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    preventive_actions = Column(String, nullable=True)
    risk_factors_detail = Column(String, nullable=True)
    insurance_guideline = Column(String, nullable=True)

