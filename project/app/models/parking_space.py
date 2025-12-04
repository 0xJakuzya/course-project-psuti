from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class ParkingSpace(Base):
    __tablename__ = "parking_spaces"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(10), nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle_type = relationship("VehicleType", back_populates="parking_spaces")
    parking_sessions = relationship("ParkingSession", back_populates="parking_space")