from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("parking_sessions.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    parking_session = relationship("ParkingSession", back_populates="payments")
    payment_method = relationship("PaymentMethod", back_populates="payments")