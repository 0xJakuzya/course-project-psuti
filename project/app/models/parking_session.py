from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class ParkingSession(Base):
    __tablename__ = "parking_sessions"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    space_id = Column(Integer, ForeignKey("parking_spaces.id"), nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"), nullable=False)
    time_in = Column(DateTime, nullable=False)
    time_out = Column(DateTime)
    total_cost = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="parking_sessions")
    parking_space = relationship("ParkingSpace", back_populates="parking_sessions")
    tariff = relationship("Tariff", back_populates="parking_sessions")
    payments = relationship("Payment", back_populates="parking_session")