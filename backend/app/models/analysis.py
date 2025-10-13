from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from app.db.session import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True, index=True)
    address = Column(String, nullable=False, index=True)
    risk_scores = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "address": self.address,
            "risk_scores": self.risk_scores,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
