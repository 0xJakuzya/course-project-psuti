from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price_per_hour = Column(DECIMAL(10, 2), nullable=False)
    price_per_day = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    parking_sessions = relationship("ParkingSession", back_populates="tariff")